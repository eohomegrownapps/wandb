"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys
import wandb.proto.wandb_base_pb2
import wandb.proto.wandb_internal_pb2

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ServerShutdownRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> None: ...

global___ServerShutdownRequest = ServerShutdownRequest

@typing_extensions.final
class ServerShutdownResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerShutdownResponse = ServerShutdownResponse

@typing_extensions.final
class ServerStatusRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> None: ...

global___ServerStatusRequest = ServerStatusRequest

@typing_extensions.final
class ServerStatusResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerStatusResponse = ServerStatusResponse

@typing_extensions.final
class StringTupleValue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STRING_VALUES_FIELD_NUMBER: builtins.int
    @property
    def string_values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        string_values: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["string_values", b"string_values"]) -> None: ...

global___StringTupleValue = StringTupleValue

@typing_extensions.final
class SettingsValue(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INT_VALUE_FIELD_NUMBER: builtins.int
    STRING_VALUE_FIELD_NUMBER: builtins.int
    FLOAT_VALUE_FIELD_NUMBER: builtins.int
    BOOL_VALUE_FIELD_NUMBER: builtins.int
    NULL_VALUE_FIELD_NUMBER: builtins.int
    TUPLE_VALUE_FIELD_NUMBER: builtins.int
    TIMESTAMP_VALUE_FIELD_NUMBER: builtins.int
    int_value: builtins.int
    string_value: builtins.str
    float_value: builtins.float
    bool_value: builtins.bool
    null_value: builtins.bool
    @property
    def tuple_value(self) -> global___StringTupleValue: ...
    timestamp_value: builtins.str
    def __init__(
        self,
        *,
        int_value: builtins.int = ...,
        string_value: builtins.str = ...,
        float_value: builtins.float = ...,
        bool_value: builtins.bool = ...,
        null_value: builtins.bool = ...,
        tuple_value: global___StringTupleValue | None = ...,
        timestamp_value: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool_value", b"bool_value", "float_value", b"float_value", "int_value", b"int_value", "null_value", b"null_value", "string_value", b"string_value", "timestamp_value", b"timestamp_value", "tuple_value", b"tuple_value", "value_type", b"value_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool_value", b"bool_value", "float_value", b"float_value", "int_value", b"int_value", "null_value", b"null_value", "string_value", b"string_value", "timestamp_value", b"timestamp_value", "tuple_value", b"tuple_value", "value_type", b"value_type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value_type", b"value_type"]) -> typing_extensions.Literal["int_value", "string_value", "float_value", "bool_value", "null_value", "tuple_value", "timestamp_value"] | None: ...

global___SettingsValue = SettingsValue

@typing_extensions.final
class ServerInformInitRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class SettingsMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___SettingsValue: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___SettingsValue | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    _SETTINGS_MAP_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _settings_map(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___SettingsValue]: ...
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _settings_map: collections.abc.Mapping[builtins.str, global___SettingsValue] | None = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "_settings_map", b"_settings_map"]) -> None: ...

global___ServerInformInitRequest = ServerInformInitRequest

@typing_extensions.final
class ServerInformInitResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformInitResponse = ServerInformInitResponse

@typing_extensions.final
class ServerInformStartRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class SettingsMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___SettingsValue: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___SettingsValue | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    _SETTINGS_MAP_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _settings_map(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___SettingsValue]: ...
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _settings_map: collections.abc.Mapping[builtins.str, global___SettingsValue] | None = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "_settings_map", b"_settings_map"]) -> None: ...

global___ServerInformStartRequest = ServerInformStartRequest

@typing_extensions.final
class ServerInformStartResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformStartResponse = ServerInformStartResponse

@typing_extensions.final
class ServerInformFinishRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> None: ...

global___ServerInformFinishRequest = ServerInformFinishRequest

@typing_extensions.final
class ServerInformFinishResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformFinishResponse = ServerInformFinishResponse

@typing_extensions.final
class ServerInformAttachRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> None: ...

global___ServerInformAttachRequest = ServerInformAttachRequest

@typing_extensions.final
class ServerInformAttachResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class SettingsMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___SettingsValue: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___SettingsValue | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    _SETTINGS_MAP_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _settings_map(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___SettingsValue]: ...
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _settings_map: collections.abc.Mapping[builtins.str, global___SettingsValue] | None = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "_settings_map", b"_settings_map"]) -> None: ...

global___ServerInformAttachResponse = ServerInformAttachResponse

@typing_extensions.final
class ServerInformDetachRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    _INFO_FIELD_NUMBER: builtins.int
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> None: ...

global___ServerInformDetachRequest = ServerInformDetachRequest

@typing_extensions.final
class ServerInformDetachResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformDetachResponse = ServerInformDetachResponse

@typing_extensions.final
class ServerInformTeardownRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXIT_CODE_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    exit_code: builtins.int
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        exit_code: builtins.int = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "exit_code", b"exit_code"]) -> None: ...

global___ServerInformTeardownRequest = ServerInformTeardownRequest

@typing_extensions.final
class ServerInformTeardownResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformTeardownResponse = ServerInformTeardownResponse

@typing_extensions.final
class ServerInformConsoleDataRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OUTPUT_TYPE_FIELD_NUMBER: builtins.int
    OUTPUT_DATA_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    output_type: builtins.str
    output_data: builtins.str
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        output_type: builtins.str = ...,
        output_data: builtins.str = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "output_data", b"output_data", "output_type", b"output_type"]) -> None: ...

global___ServerInformConsoleDataRequest = ServerInformConsoleDataRequest

@typing_extensions.final
class ServerInformConsoleDataResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformConsoleDataResponse = ServerInformConsoleDataResponse

@typing_extensions.final
class ServerInformConsoleStartRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RUN_ID_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    run_id: builtins.str
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        run_id: builtins.str = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "run_id", b"run_id"]) -> None: ...

global___ServerInformConsoleStartRequest = ServerInformConsoleStartRequest

@typing_extensions.final
class ServerInformConsoleStartResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformConsoleStartResponse = ServerInformConsoleStartResponse

@typing_extensions.final
class ServerInformConsoleStopRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RUN_ID_FIELD_NUMBER: builtins.int
    _INFO_FIELD_NUMBER: builtins.int
    run_id: builtins.str
    @property
    def _info(self) -> wandb.proto.wandb_base_pb2._RecordInfo: ...
    def __init__(
        self,
        *,
        run_id: builtins.str = ...,
        _info: wandb.proto.wandb_base_pb2._RecordInfo | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_info", b"_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_info", b"_info", "run_id", b"run_id"]) -> None: ...

global___ServerInformConsoleStopRequest = ServerInformConsoleStopRequest

@typing_extensions.final
class ServerInformConsoleStopResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ServerInformConsoleStopResponse = ServerInformConsoleStopResponse

@typing_extensions.final
class ServerRequest(google.protobuf.message.Message):
    """
    ServerRequest, ServerResponse: used in sock server
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RECORD_PUBLISH_FIELD_NUMBER: builtins.int
    RECORD_COMMUNICATE_FIELD_NUMBER: builtins.int
    INFORM_INIT_FIELD_NUMBER: builtins.int
    INFORM_FINISH_FIELD_NUMBER: builtins.int
    INFORM_ATTACH_FIELD_NUMBER: builtins.int
    INFORM_DETACH_FIELD_NUMBER: builtins.int
    INFORM_TEARDOWN_FIELD_NUMBER: builtins.int
    INFORM_START_FIELD_NUMBER: builtins.int
    INFORM_CONSOLE_DATA_FIELD_NUMBER: builtins.int
    INFORM_CONSOLE_START_FIELD_NUMBER: builtins.int
    INFORM_CONSOLE_STOP_FIELD_NUMBER: builtins.int
    @property
    def record_publish(self) -> wandb.proto.wandb_internal_pb2.Record: ...
    @property
    def record_communicate(self) -> wandb.proto.wandb_internal_pb2.Record: ...
    @property
    def inform_init(self) -> global___ServerInformInitRequest: ...
    @property
    def inform_finish(self) -> global___ServerInformFinishRequest: ...
    @property
    def inform_attach(self) -> global___ServerInformAttachRequest: ...
    @property
    def inform_detach(self) -> global___ServerInformDetachRequest: ...
    @property
    def inform_teardown(self) -> global___ServerInformTeardownRequest: ...
    @property
    def inform_start(self) -> global___ServerInformStartRequest: ...
    @property
    def inform_console_data(self) -> global___ServerInformConsoleDataRequest: ...
    @property
    def inform_console_start(self) -> global___ServerInformConsoleStartRequest: ...
    @property
    def inform_console_stop(self) -> global___ServerInformConsoleStopRequest: ...
    def __init__(
        self,
        *,
        record_publish: wandb.proto.wandb_internal_pb2.Record | None = ...,
        record_communicate: wandb.proto.wandb_internal_pb2.Record | None = ...,
        inform_init: global___ServerInformInitRequest | None = ...,
        inform_finish: global___ServerInformFinishRequest | None = ...,
        inform_attach: global___ServerInformAttachRequest | None = ...,
        inform_detach: global___ServerInformDetachRequest | None = ...,
        inform_teardown: global___ServerInformTeardownRequest | None = ...,
        inform_start: global___ServerInformStartRequest | None = ...,
        inform_console_data: global___ServerInformConsoleDataRequest | None = ...,
        inform_console_start: global___ServerInformConsoleStartRequest | None = ...,
        inform_console_stop: global___ServerInformConsoleStopRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["inform_attach", b"inform_attach", "inform_console_data", b"inform_console_data", "inform_console_start", b"inform_console_start", "inform_console_stop", b"inform_console_stop", "inform_detach", b"inform_detach", "inform_finish", b"inform_finish", "inform_init", b"inform_init", "inform_start", b"inform_start", "inform_teardown", b"inform_teardown", "record_communicate", b"record_communicate", "record_publish", b"record_publish", "server_request_type", b"server_request_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["inform_attach", b"inform_attach", "inform_console_data", b"inform_console_data", "inform_console_start", b"inform_console_start", "inform_console_stop", b"inform_console_stop", "inform_detach", b"inform_detach", "inform_finish", b"inform_finish", "inform_init", b"inform_init", "inform_start", b"inform_start", "inform_teardown", b"inform_teardown", "record_communicate", b"record_communicate", "record_publish", b"record_publish", "server_request_type", b"server_request_type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["server_request_type", b"server_request_type"]) -> typing_extensions.Literal["record_publish", "record_communicate", "inform_init", "inform_finish", "inform_attach", "inform_detach", "inform_teardown", "inform_start", "inform_console_data", "inform_console_start", "inform_console_stop"] | None: ...

global___ServerRequest = ServerRequest

@typing_extensions.final
class ServerResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULT_COMMUNICATE_FIELD_NUMBER: builtins.int
    INFORM_INIT_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_FINISH_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_ATTACH_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_DETACH_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_TEARDOWN_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_START_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_CONSOLE_DATA_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_CONSOLE_START_RESPONSE_FIELD_NUMBER: builtins.int
    INFORM_CONSOLE_STOP_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def result_communicate(self) -> wandb.proto.wandb_internal_pb2.Result: ...
    @property
    def inform_init_response(self) -> global___ServerInformInitResponse: ...
    @property
    def inform_finish_response(self) -> global___ServerInformFinishResponse: ...
    @property
    def inform_attach_response(self) -> global___ServerInformAttachResponse: ...
    @property
    def inform_detach_response(self) -> global___ServerInformDetachResponse: ...
    @property
    def inform_teardown_response(self) -> global___ServerInformTeardownResponse: ...
    @property
    def inform_start_response(self) -> global___ServerInformStartResponse: ...
    @property
    def inform_console_data_response(self) -> global___ServerInformConsoleDataResponse: ...
    @property
    def inform_console_start_response(self) -> global___ServerInformConsoleStartResponse: ...
    @property
    def inform_console_stop_response(self) -> global___ServerInformConsoleStopResponse: ...
    def __init__(
        self,
        *,
        result_communicate: wandb.proto.wandb_internal_pb2.Result | None = ...,
        inform_init_response: global___ServerInformInitResponse | None = ...,
        inform_finish_response: global___ServerInformFinishResponse | None = ...,
        inform_attach_response: global___ServerInformAttachResponse | None = ...,
        inform_detach_response: global___ServerInformDetachResponse | None = ...,
        inform_teardown_response: global___ServerInformTeardownResponse | None = ...,
        inform_start_response: global___ServerInformStartResponse | None = ...,
        inform_console_data_response: global___ServerInformConsoleDataResponse | None = ...,
        inform_console_start_response: global___ServerInformConsoleStartResponse | None = ...,
        inform_console_stop_response: global___ServerInformConsoleStopResponse | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["inform_attach_response", b"inform_attach_response", "inform_console_data_response", b"inform_console_data_response", "inform_console_start_response", b"inform_console_start_response", "inform_console_stop_response", b"inform_console_stop_response", "inform_detach_response", b"inform_detach_response", "inform_finish_response", b"inform_finish_response", "inform_init_response", b"inform_init_response", "inform_start_response", b"inform_start_response", "inform_teardown_response", b"inform_teardown_response", "result_communicate", b"result_communicate", "server_response_type", b"server_response_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["inform_attach_response", b"inform_attach_response", "inform_console_data_response", b"inform_console_data_response", "inform_console_start_response", b"inform_console_start_response", "inform_console_stop_response", b"inform_console_stop_response", "inform_detach_response", b"inform_detach_response", "inform_finish_response", b"inform_finish_response", "inform_init_response", b"inform_init_response", "inform_start_response", b"inform_start_response", "inform_teardown_response", b"inform_teardown_response", "result_communicate", b"result_communicate", "server_response_type", b"server_response_type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["server_response_type", b"server_response_type"]) -> typing_extensions.Literal["result_communicate", "inform_init_response", "inform_finish_response", "inform_attach_response", "inform_detach_response", "inform_teardown_response", "inform_start_response", "inform_console_data_response", "inform_console_start_response", "inform_console_stop_response"] | None: ...

global___ServerResponse = ServerResponse
