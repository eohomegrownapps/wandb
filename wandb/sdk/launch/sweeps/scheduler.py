"""Abstract Scheduler class."""
import base64
import logging
import os
import socket
import time
import yaml
import threading
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Tuple

import click

import wandb
import wandb.apis.public as public
from wandb.apis.internal import Api
from wandb.errors import CommError
from wandb.sdk.launch.launch_add import launch_add
from wandb.sdk.launch.sweeps import SchedulerError
from wandb.sdk.lib.runid import generate_id
from wandb.sdk.wandb_run import Run as SdkRun
from wandb.wandb_agent import Agent, _create_sweep_command_args

_logger = logging.getLogger(__name__)
LOG_PREFIX = f"{click.style('sched:', fg='cyan')} "


@dataclass
class _Worker:
    agent_config: Dict[str, Any]
    agent_id: str
    run_id: str


class SchedulerState(Enum):
    PENDING = 0
    STARTING = 1
    RUNNING = 2
    FLUSH_RUNS = 3
    COMPLETED = 4
    FAILED = 5
    STOPPED = 6
    CANCELLED = 7


class RunState(Enum):
    ALIVE = 0
    DEAD = 1
    UNKNOWN = 2


@dataclass
class SweepRun:
    id: str
    worker_id: int
    state: RunState = RunState.ALIVE
    queued_run: Optional[public.QueuedRun] = None
    args: Optional[Dict[str, Any]] = None
    logs: Optional[List[str]] = None


class Scheduler(ABC):
    """A controller/agent that populates a Launch RunQueue from a hyperparameter sweep."""

    def __init__(
        self,
        api: Api,
        *args: Optional[Any],
        sweep_id: Optional[str] = None,
        entity: Optional[str] = None,
        project: Optional[str] = None,
        project_queue: Optional[str] = None,
        **kwargs: Optional[Any],
    ):
        self._api = api
        self._entity = (
            entity
            or os.environ.get("WANDB_ENTITY")
            or api.settings("entity")
            or api.default_entity
        )
        self._project = (
            project or os.environ.get("WANDB_PROJECT") or api.settings("project")
        )
        self._sweep_id: str = sweep_id or "empty-sweep-id"
        self._state: SchedulerState = SchedulerState.PENDING

        # Make sure the provided sweep_id corresponds to a valid sweep
        try:
            resp = self._api.sweep(
                sweep_id, "{}", entity=self._entity, project=self._project
            )
            if resp.get("state") == SchedulerState.CANCELLED.name:
                self._state = SchedulerState.CANCELLED
            self._sweep_config = yaml.safe_load(resp["config"])
        except Exception as e:
            raise SchedulerError(f"{LOG_PREFIX}Exception when finding sweep: {e}")

        # Dictionary of the runs being managed by the scheduler
        self._runs: Dict[str, SweepRun] = {}
        # Threading lock to ensure thread-safe access to the runs dictionary
        self._threading_lock: threading.Lock = threading.Lock()
        self._project_queue = project_queue
        # Optionally run multiple workers in (pseudo-)parallel. Workers do not
        # actually run training workloads, they simply send heartbeat messages
        # (emulating a real agent) and add new runs to the launch queue. The
        # launch agent is the one that actually runs the training workloads.
        self._workers: Dict[int, _Worker] = {}

        # Scheduler may receive additional kwargs which will be piped into the launch command
        self._kwargs: Dict[str, Any] = kwargs

    @abstractmethod
    def _get_next_sweep_run(self, worker_id: int) -> Optional[SweepRun]:
        pass

    @abstractmethod
    def _exit(self) -> None:
        pass

    @property
    def state(self) -> SchedulerState:
        _logger.debug(f"{LOG_PREFIX}Scheduler state is {self._state.name}")
        return self._state

    @state.setter
    def state(self, value: SchedulerState) -> None:
        _logger.debug(f"{LOG_PREFIX}Scheduler was {self.state.name} is {value.name}")
        self._state = value

    @property
    def is_alive(self) -> bool:
        if self.state in [
            SchedulerState.COMPLETED,
            SchedulerState.FAILED,
            SchedulerState.STOPPED,
            SchedulerState.CANCELLED,
        ]:
            return False
        return True

    @property
    def num_active_runs(self) -> int:
        return len(self._runs)

    @property
    def busy_workers(self) -> Dict[int, _Worker]:
        """
        Returns dict of id:worker already assigned to a launch run

        runs should always have a worker_id, but are created before
        workers are assigned to the run
        """
        busy_workers = {}
        for _, r in self._yield_runs():
            busy_workers[r.worker_id] = self._workers[r.worker_id]
        return busy_workers

    @property
    def available_workers(self) -> Dict[int, _Worker]:
        """
        Returns dict of id:worker ready to launch another run
        """
        return {_id: w for _id, w in self._workers if _id not in self.busy_workers}

    def _init_wandb_run(self) -> SdkRun:
        """
        Controls resume or init logic for a scheduler wandb run
        """
        if self._kwargs.get("run_id"):  # resume
            return wandb.init(resume=self._kwargs["run_id"])

        name = self._kwargs.get("sweep_type")

        return wandb.init(name=f"{name}-scheduler-{self._sweep_id}", resume="allow")

    def start(self) -> None:
        """Start a scheduler, confirms prerequisites, begins execution loop."""
        wandb.termlog(f"{LOG_PREFIX}Scheduler starting.")
        if not self.is_alive:
            wandb.termerror(
                f"{LOG_PREFIX}Sweep already in completed state ({self.state.name.lower()}). Exiting..."
            )
            self.exit()
            return

        self._state = SchedulerState.STARTING
        if not self._try_load_executable():
            wandb.termerror(
                f"{LOG_PREFIX}No 'job' or 'image_uri' loaded from sweep config."
            )
            self.exit()
            return

        self._load_state()
        self._register_agents()
        self.run()

    def run(self) -> None:
        """Main run function."""
        wandb.termlog(f"{LOG_PREFIX}Scheduler running")
        self.state = SchedulerState.RUNNING
        try:
            while True:
                wandb.termlog(f"{LOG_PREFIX}Polling for new runs to launch")
                if not self.is_alive:
                    break

                self._update_run_states()
                if self.state == SchedulerState.FLUSH_RUNS:
                    if self.num_active_runs == 0:
                        wandb.termlog(f"{LOG_PREFIX}Done polling on runs, exiting")
                        break
                    time.sleep(self._polling_sleep)
                    continue

                for worker_id in self.available_workers:
                    run: Optional[SweepRun] = self._get_next_sweep_run(worker_id)
                    if not run:
                        break

                    self._add_to_launch_queue(run)

                time.sleep(self._polling_sleep)
        except KeyboardInterrupt:
            wandb.termwarn(f"{LOG_PREFIX}Scheduler received KeyboardInterrupt. Exiting")
            self.state = SchedulerState.STOPPED
            self.exit()
            return
        except Exception as e:
            wandb.termlog(f"{LOG_PREFIX}Scheduler failed with exception {e}")
            self.state = SchedulerState.FAILED
            self.exit()
            raise e
        else:
            wandb.termlog(f"{LOG_PREFIX}Scheduler completed")
            self.exit()

    def exit(self) -> None:
        self._exit()
        if self.state not in [
            SchedulerState.COMPLETED,
            SchedulerState.STOPPED,
        ]:
            self.state = SchedulerState.FAILED
        self._stop_runs()

    def _try_load_executable(self) -> bool:
        """
        Check existance of valid executable for a run.

        logs and returns False when job is unreachable
        """
        if self._kwargs.get("job"):
            _public_api = public.Api()
            try:
                _job_artifact = _public_api.artifact(self._kwargs["job"], type="job")
                wandb.termlog(
                    f"{LOG_PREFIX}Successfully loaded job ({_job_artifact.name}) in scheduler"
                )
            except Exception:
                wandb.termerror(f"{LOG_PREFIX}{traceback.format_exc()}")
                return False
            return True
        elif self._kwargs.get("image_uri"):
            # TODO(gst): check docker existance? Use registry in launch config?
            return True
        else:
            return False

    def _register_agents(self) -> None:
        for worker_id in range(self._num_workers):
            _logger.debug(f"{LOG_PREFIX}Starting AgentHeartbeat worker ({worker_id})")
            agent_config = self._api.register_agent(
                f"{socket.gethostname()}-{worker_id}",  # host
                sweep_id=self._sweep_id,
                project_name=self._project,
                entity=self._entity,
            )
            self._workers[worker_id] = _Worker(
                agent_config=agent_config,
                agent_id=agent_config["id"],
            )

    def _yield_runs(self) -> Iterator[Tuple[str, SweepRun]]:
        """Thread-safe way to iterate over the runs."""
        with self._threading_lock:
            yield from self._runs.items()

    def _stop_runs(self) -> None:
        to_delete = []
        for run_id, _ in self._yield_runs():
            to_delete += [run_id]

        for run_id in to_delete:
            wandb.termlog(f"{LOG_PREFIX}Stopping run ({run_id})")
            self._stop_run(run_id)

    def _stop_run(self, run_id: str) -> bool:
        """Stops a run and removes it from the scheduler"""
        if run_id in self._yield_runs():
            run = self._runs[run_id]
            run.state = RunState.DEAD

            if not run.queued_run:
                _logger.debug(f"tried to _stop_run but run ({run.id}) not queued yet")
                return False

            encoded_run_id = base64.standard_b64encode(
                f"Run:v1:{run_id}:{self._project}:{self._entity}".encode()
            ).decode("utf-8")

            # TODO(gst): improve performance here
            success = self._api.stop_run(run_id=encoded_run_id)
            if success:
                wandb.termlog(f"{LOG_PREFIX}Stopped run ({run_id})")
            else:
                wandb.termlog(f"{LOG_PREFIX}Failed while stopping run ({run_id})")

            del self._runs[run_id]

            return success

    def _update_run_states(self) -> None:
        """Iterate through runs.

        Get state from backend and deletes runs if not in running state. Threadsafe.
        """
        _runs_to_remove: List[str] = []
        for run_id, run in self._yield_runs():
            try:
                _state = self._api.get_run_state(self._entity, self._project, run_id)
                _rqi_state = run.queued_run.state if run.queued_run else None
                if (
                    not _state
                    or _state
                    in [
                        "crashed",
                        "failed",
                        "killed",
                        "finished",
                    ]
                    or _rqi_state == "failed"
                ):
                    _logger.debug(
                        f"({run_id}) run-state:{_state}, rqi-state:{_rqi_state}"
                    )
                    run.state = RunState.DEAD
                    _runs_to_remove.append(run_id)
                elif _state in [
                    "running",
                    "pending",
                    "preempted",
                    "preempting",
                ]:
                    run.state = RunState.ALIVE
            except CommError as e:
                _logger.debug(
                    f"Issue when getting state for run ({run_id}) with error: {e}"
                )
                run.state = RunState.UNKNOWN
                continue
        # Remove any runs that are dead
        with self._threading_lock:
            for run_id in _runs_to_remove:
                wandb.termlog(f"{LOG_PREFIX}Cleaning up finished run {run_id}.")
                del self._runs[run_id]

    def _add_to_launch_queue(self, run: SweepRun) -> "public.QueuedRun":
        """Add a launch job to the Launch RunQueue"""
        # job and image first from CLI args, then from sweep config
        _job = self._kwargs.get("job") or self._sweep_config.get("job")

        _sweep_config_uri = self._sweep_config.get("image_uri")
        _image_uri = self._kwargs.get("image_uri") or _sweep_config_uri
        if _job is None and _image_uri is None:
            raise SchedulerError(
                f"{LOG_PREFIX}No 'job' nor 'image_uri' (run: {run.id})"
            )
        elif _job is not None and _image_uri is not None:
            raise SchedulerError(f"{LOG_PREFIX}Sweep has both 'job' and 'image_uri'")

        if self._sweep_config.get("command"):
            entry_point = Agent._create_sweep_command(self._sweep_config["command"])
            wandb.termwarn(
                f"{LOG_PREFIX}Sweep command {entry_point} will override"
                f' {"job" if _job else "image_uri"} entrypoint'
            )

        _args = _create_sweep_command_args({"args": run.args})["args_dict"]
        launch_config = {"overrides": {"run_config": _args}}

        run_id = run.id or generate_id()
        queued_run = launch_add(
            run_id=run_id,
            entry_point=entry_point,
            config=launch_config,
            docker_image=_image_uri,  # TODO(gst): make agnostic (github? run uri?)
            job=_job,
            project=self._project,
            entity=self._entity,
            queue_name=self._kwargs.get("queue"),
            project_queue=self._project_queue,
            resource=self._kwargs.get("resource", None),
            resource_args=self._kwargs.get("resource_args", None),
        )
        run.queued_run = queued_run
        self._runs[run_id] = run
        wandb.termlog(
            f"{LOG_PREFIX}Added run ({run_id}) to queue ({self._kwargs.get('queue')})"
        )
        return queued_run
