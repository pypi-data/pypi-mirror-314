from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DocType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PDF: _ClassVar[DocType]
    JPG: _ClassVar[DocType]
    PNG: _ClassVar[DocType]
    PDF_SCAN: _ClassVar[DocType]
PDF: DocType
JPG: DocType
PNG: DocType
PDF_SCAN: DocType

class DigitalAssistantOCRResponse(_message.Message):
    __slots__ = ("Text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    Text: str
    def __init__(self, Text: _Optional[str] = ...) -> None: ...

class DigitalAssistantOCRRequest(_message.Message):
    __slots__ = ("Document", "Type")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    Document: bytes
    Type: DocType
    def __init__(self, Document: _Optional[bytes] = ..., Type: _Optional[_Union[DocType, str]] = ...) -> None: ...
