from google.protobuf import empty_pb2 as _empty_pb2
from kr8_protobuf import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("_id", "first_name", "last_name", "email", "type", "profile_picture", "verified")
    _ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_FIELD_NUMBER: _ClassVar[int]
    VERIFIED_FIELD_NUMBER: _ClassVar[int]
    _id: str
    first_name: str
    last_name: str
    email: str
    type: UserType
    profile_picture: _common_pb2.Document
    verified: bool
    def __init__(self, _id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email: _Optional[str] = ..., type: _Optional[_Union[UserType, _Mapping]] = ..., profile_picture: _Optional[_Union[_common_pb2.Document, _Mapping]] = ..., verified: bool = ...) -> None: ...

class UserType(_message.Message):
    __slots__ = ("_id", "label")
    _ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    _id: str
    label: str
    def __init__(self, _id: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...
