"""Abstract Scheduler class."""
import base64
import logging
import os
import yaml
import threading
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
from wandb.sdk.launch.utils import LAUNCH_DEFAULT_PROJECT

logger = logging.getLogger(__name__)
LOG_PREFIX = f"{click.style('sched:', fg='cyan')} "


class SchedulerState(Enum):
    PENDING = 0
    STARTING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    STOPPED = 5


class SimpleRunState(Enum):
    ALIVE = 0
    DEAD = 1
    UNKNOWN = 2


@dataclass
class SweepRun:
    id: str
    state: SimpleRunState = SimpleRunState.ALIVE
    queued_run: Optional[public.QueuedRun] = None
    args: Optional[Dict[str, Any]] = None
    logs: Optional[List[str]] = None
    program: Optional[str] = None
    # Threading can be used to run multiple workers in parallel
    worker_id: Optional[int] = None


class Scheduler(ABC):
    """The Scheduler is a controller/agent that will populate a Launch RunQueue
    with jobs from a hyperparameter sweep.
    """

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
        # Make sure the provided sweep_id corresponds to a valid sweep
        try:
            raw = self._api.sweep(
                sweep_id, "{}", entity=self._entity, project=self._project
            )
            self._sweep_config = yaml.safe_load(raw["config"])
        except Exception as e:
            raise SchedulerError(f"{LOG_PREFIX}Exception when finding sweep: {e}")
        self._sweep_id: str = sweep_id or "empty-sweep-id"
        self._state: SchedulerState = SchedulerState.PENDING
        # Dictionary of the runs being managed by the scheduler
        self._runs: Dict[str, SweepRun] = {}
        # Threading lock to ensure thread-safe access to the runs dictionary
        self._threading_lock: threading.Lock = threading.Lock()
        self._project_queue = project_queue
        # Queue args
        self._queue_sleep = 1.0
        self._queue_timeout = 1.0
        # Scheduler may receive additional kwargs which will be piped into the launch command
        self._kwargs: Dict[str, Any] = kwargs

    @abstractmethod
    def _start(self) -> None:
        pass

    @abstractmethod
    def _run(self) -> None:
        pass

    @abstractmethod
    def _exit(self) -> None:
        pass

    @property
    def state(self) -> SchedulerState:
        logger.debug(f"{LOG_PREFIX}Scheduler state is {self._state.name}")
        return self._state

    @state.setter
    def state(self, value: SchedulerState) -> None:
        logger.debug(f"{LOG_PREFIX}Scheduler was {self.state.name} is {value.name}")
        self._state = value

    def is_alive(self) -> bool:
        if self.state in [
            SchedulerState.COMPLETED,
            SchedulerState.FAILED,
            SchedulerState.STOPPED,
        ]:
            return False
        return True

    def start(self) -> None:
        wandb.termlog(f"{LOG_PREFIX}Scheduler starting.")
        self._state = SchedulerState.STARTING
        self._start()
        self.run()

    def run(self) -> None:
        wandb.termlog(f"{LOG_PREFIX}Scheduler Running.")
        self.state = SchedulerState.RUNNING
        try:
            while True:
                if not self.is_alive():
                    break
                self._update_run_states()
                self._run()
        except KeyboardInterrupt:
            wandb.termlog(f"{LOG_PREFIX}Scheduler received KeyboardInterrupt. Exiting.")
            self.state = SchedulerState.STOPPED
            self.exit()
            return
        except Exception as e:
            wandb.termlog(f"{LOG_PREFIX}Scheduler failed with exception {e}")
            self.state = SchedulerState.FAILED
            self.exit()
            raise e
        else:
            wandb.termlog(f"{LOG_PREFIX}Scheduler completed.")
            self.exit()

    def exit(self) -> None:
        self._exit()
        if self.state not in [
            SchedulerState.COMPLETED,
            SchedulerState.STOPPED,
        ]:
            self.state = SchedulerState.FAILED
        self._stop_runs()

    def _yield_runs(self) -> Iterator[Tuple[str, SweepRun]]:
        """Thread-safe way to iterate over the runs."""
        with self._threading_lock:
            yield from self._runs.items()

    def _stop_runs(self) -> None:
        for run_id, _ in self._yield_runs():
            wandb.termlog(f"{LOG_PREFIX}Stopping run {run_id}.")
            self._stop_run(run_id)

    def _stop_run(self, run_id: str) -> bool:
        """Stops a run and removes it from the scheduler"""
        if run_id in self._runs:
            run: SweepRun = self._runs[run_id]
            run.state = SimpleRunState.DEAD

            if not run.queued_run:
                logging.debug(f"tried to _stop_run but run not queued yet (run_id:{run.id})")

            encoded_run_id = base64.standard_b64encode(
                f"Run:v1:{run_id}:{self._project}:{self._entity}".encode()
            ).decode("utf-8")

            print(f"{encoded_run_id=}")

            success = self._api.stop_run(run_id)
            if success:
                wandb.termlog(f"{LOG_PREFIX} Stopped run {run_id}.")
            else:
                wandb.termlog(f"{LOG_PREFIX} Failed while stopping run {run_id}.")

            del self._runs[run_id]

            return success

    def _update_run_states(self) -> None:
        _runs_to_remove: List[str] = []
        for run_id, run in self._yield_runs():                
            try:
                _state = self._api.get_run_state(self._entity, self._project, run_id)
                if _state is None or _state in [
                    "crashed",
                    "failed",
                    "killed",
                    "finished",
                ]:
                    run.state = SimpleRunState.DEAD
                    _runs_to_remove.append(run_id)
                elif _state in [
                    "running",
                    "pending",
                    "preempted",
                    "preempting",
                ]:
                    run.state = SimpleRunState.ALIVE
            except CommError as e:
                logging.debug(
                    f"{LOG_PREFIX}Issue when getting RunState for Run {run_id}: {e}"
                )
                run.state = SimpleRunState.UNKNOWN
                continue
        # Remove any runs that are dead
        with self._threading_lock:
            for run_id in _runs_to_remove:
                wandb.termlog(f"{LOG_PREFIX}Cleaning up dead run {run_id}.")
                del self._runs[run_id]

    def _add_to_launch_queue(
        self,
        run_id: Optional[str] = None,
        entry_point: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> "public.QueuedRun":
        """Add a launch job to the Launch RunQueue."""
        run_id = run_id or generate_id()
        # One of Job is required
        _job = self._kwargs.get("job", None)
        if _job is None:
            wandb.termwarn("A launch sweep config must contain a job to execute")
            self.exit()

        # Queue is required
        _queue = self._kwargs.get("queue", "default")

        queued_run = launch_add(
            run_id=run_id,
            entry_point=entry_point,
            config=config,
            job=_job,
            project=self._project,
            entity=self._entity,
            queue_name=_queue,
            project_queue=self._project_queue,
            resource=self._kwargs.get("resource", None),
            resource_args=self._kwargs.get("resource_args", None),
            sweep_id=self._sweep_id,
        )
        self._runs[run_id].queued_run = queued_run
        wandb.termlog(
            f"{LOG_PREFIX}Added run to Launch RunQueue: {_queue} RunID:{run_id}."
        )
        return queued_run
