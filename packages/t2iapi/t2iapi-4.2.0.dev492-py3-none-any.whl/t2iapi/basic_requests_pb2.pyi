from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BasicHandleRequest(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: str
    def __init__(self, handle: _Optional[str] = ...) -> None: ...

class RepeatedStringRequest(_message.Message):
    __slots__ = ("repeated_string",)
    REPEATED_STRING_FIELD_NUMBER: _ClassVar[int]
    repeated_string: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, repeated_string: _Optional[_Iterable[str]] = ...) -> None: ...
