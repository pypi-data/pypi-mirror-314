from kr8_protobuf import common_pb2 as _common_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageRequest(_message.Message):
    __slots__ = ("topic", "notification", "data_json", "android", "apns")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    DATA_JSON_FIELD_NUMBER: _ClassVar[int]
    ANDROID_FIELD_NUMBER: _ClassVar[int]
    APNS_FIELD_NUMBER: _ClassVar[int]
    topic: str
    notification: Notification
    data_json: str
    android: Android
    apns: Apns
    def __init__(self, topic: _Optional[str] = ..., notification: _Optional[_Union[Notification, _Mapping]] = ..., data_json: _Optional[str] = ..., android: _Optional[_Union[Android, _Mapping]] = ..., apns: _Optional[_Union[Apns, _Mapping]] = ...) -> None: ...

class Notification(_message.Message):
    __slots__ = ("title", "body")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    title: str
    body: str
    def __init__(self, title: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class Android(_message.Message):
    __slots__ = ("notification",)
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    notification: AndroidNotification
    def __init__(self, notification: _Optional[_Union[AndroidNotification, _Mapping]] = ...) -> None: ...

class AndroidNotification(_message.Message):
    __slots__ = ("click_action",)
    CLICK_ACTION_FIELD_NUMBER: _ClassVar[int]
    click_action: str
    def __init__(self, click_action: _Optional[str] = ...) -> None: ...

class Apns(_message.Message):
    __slots__ = ("payload",)
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: Payload
    def __init__(self, payload: _Optional[_Union[Payload, _Mapping]] = ...) -> None: ...

class Payload(_message.Message):
    __slots__ = ("aps",)
    APS_FIELD_NUMBER: _ClassVar[int]
    aps: Aps
    def __init__(self, aps: _Optional[_Union[Aps, _Mapping]] = ...) -> None: ...

class Aps(_message.Message):
    __slots__ = ("category",)
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    category: str
    def __init__(self, category: _Optional[str] = ...) -> None: ...
