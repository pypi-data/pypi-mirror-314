from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetResourceProviderCountRequest(_message.Message):
    __slots__ = ("workspace_id", "environment_id", "resource")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    environment_id: str
    resource: str
    def __init__(self, workspace_id: _Optional[str] = ..., environment_id: _Optional[str] = ..., resource: _Optional[str] = ...) -> None: ...

class GetResourceProviderCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class CompletionRequest(_message.Message):
    __slots__ = ("workspace_id", "environment_id", "primary", "secondary_model_index", "resource", "stream", "messages", "tools", "tool_choice", "config", "include_raw_response", "resource_config_overrides", "metadata")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_MODEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    TOOL_CHOICE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_RAW_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CONFIG_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    environment_id: str
    primary: bool
    secondary_model_index: int
    resource: str
    stream: bool
    messages: _containers.RepeatedCompositeFieldContainer[RequestMessage]
    tools: _containers.RepeatedCompositeFieldContainer[RequestTools]
    tool_choice: RequestToolChoice
    config: _struct_pb2.Struct
    include_raw_response: bool
    resource_config_overrides: _struct_pb2.Struct
    metadata: _struct_pb2.Struct
    def __init__(self, workspace_id: _Optional[str] = ..., environment_id: _Optional[str] = ..., primary: bool = ..., secondary_model_index: _Optional[int] = ..., resource: _Optional[str] = ..., stream: bool = ..., messages: _Optional[_Iterable[_Union[RequestMessage, _Mapping]]] = ..., tools: _Optional[_Iterable[_Union[RequestTools, _Mapping]]] = ..., tool_choice: _Optional[_Union[RequestToolChoice, _Mapping]] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., include_raw_response: bool = ..., resource_config_overrides: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RequestMessage(_message.Message):
    __slots__ = ("name", "role", "content", "tool_calls", "tool_call_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALL_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    role: str
    content: str
    tool_calls: _containers.RepeatedCompositeFieldContainer[RequestMessageToolCall]
    tool_call_id: str
    def __init__(self, name: _Optional[str] = ..., role: _Optional[str] = ..., content: _Optional[str] = ..., tool_calls: _Optional[_Iterable[_Union[RequestMessageToolCall, _Mapping]]] = ..., tool_call_id: _Optional[str] = ...) -> None: ...

class RequestMessageToolCall(_message.Message):
    __slots__ = ("id", "type", "function")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    function: RequestMessageToolCallFunction
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., function: _Optional[_Union[RequestMessageToolCallFunction, _Mapping]] = ...) -> None: ...

class RequestMessageToolCallFunction(_message.Message):
    __slots__ = ("name", "arguments")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    arguments: str
    def __init__(self, name: _Optional[str] = ..., arguments: _Optional[str] = ...) -> None: ...

class RequestTools(_message.Message):
    __slots__ = ("type", "function")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    type: str
    function: RequestToolFunction
    def __init__(self, type: _Optional[str] = ..., function: _Optional[_Union[RequestToolFunction, _Mapping]] = ...) -> None: ...

class RequestToolFunction(_message.Message):
    __slots__ = ("name", "description", "parameters")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    parameters: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RequestToolChoice(_message.Message):
    __slots__ = ("auto", "none", "tool")
    AUTO_FIELD_NUMBER: _ClassVar[int]
    NONE_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    auto: bool
    none: bool
    tool: RequestToolChoiceItem
    def __init__(self, auto: bool = ..., none: bool = ..., tool: _Optional[_Union[RequestToolChoiceItem, _Mapping]] = ...) -> None: ...

class RequestToolChoiceItem(_message.Message):
    __slots__ = ("type", "function")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    type: str
    function: RequestToolChoiceFunction
    def __init__(self, type: _Optional[str] = ..., function: _Optional[_Union[RequestToolChoiceFunction, _Mapping]] = ...) -> None: ...

class RequestToolChoiceFunction(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ("id", "message", "role", "tool_calls", "usage", "response_timestamp", "metadata", "metrics", "raw_response", "finish_reason")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    RAW_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: str
    role: str
    tool_calls: _containers.RepeatedCompositeFieldContainer[RequestMessageToolCall]
    usage: CompletionUsage
    response_timestamp: int
    metadata: CompletionResponseMetadata
    metrics: CompletionResponseMetrics
    raw_response: _struct_pb2.Struct
    finish_reason: str
    def __init__(self, id: _Optional[str] = ..., message: _Optional[str] = ..., role: _Optional[str] = ..., tool_calls: _Optional[_Iterable[_Union[RequestMessageToolCall, _Mapping]]] = ..., usage: _Optional[_Union[CompletionUsage, _Mapping]] = ..., response_timestamp: _Optional[int] = ..., metadata: _Optional[_Union[CompletionResponseMetadata, _Mapping]] = ..., metrics: _Optional[_Union[CompletionResponseMetrics, _Mapping]] = ..., raw_response: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., finish_reason: _Optional[str] = ...) -> None: ...

class CompletionUsage(_message.Message):
    __slots__ = ("prompt", "completion", "total")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    prompt: int
    completion: int
    total: int
    def __init__(self, prompt: _Optional[int] = ..., completion: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class CompletionResponseMetadata(_message.Message):
    __slots__ = ("primary", "secondary_model_index", "provider", "model", "done", "success", "fallback", "fallback_attempts", "error_message", "error_code", "error_reason")
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_MODEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_REASON_FIELD_NUMBER: _ClassVar[int]
    primary: bool
    secondary_model_index: int
    provider: str
    model: str
    done: bool
    success: bool
    fallback: bool
    fallback_attempts: int
    error_message: str
    error_code: int
    error_reason: str
    def __init__(self, primary: bool = ..., secondary_model_index: _Optional[int] = ..., provider: _Optional[str] = ..., model: _Optional[str] = ..., done: bool = ..., success: bool = ..., fallback: bool = ..., fallback_attempts: _Optional[int] = ..., error_message: _Optional[str] = ..., error_code: _Optional[int] = ..., error_reason: _Optional[str] = ...) -> None: ...

class CompletionResponseMetrics(_message.Message):
    __slots__ = ("time_to_first_token", "tokens_per_second", "duration", "provider_duration")
    TIME_TO_FIRST_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKENS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_DURATION_FIELD_NUMBER: _ClassVar[int]
    time_to_first_token: float
    tokens_per_second: float
    duration: float
    provider_duration: float
    def __init__(self, time_to_first_token: _Optional[float] = ..., tokens_per_second: _Optional[float] = ..., duration: _Optional[float] = ..., provider_duration: _Optional[float] = ...) -> None: ...
