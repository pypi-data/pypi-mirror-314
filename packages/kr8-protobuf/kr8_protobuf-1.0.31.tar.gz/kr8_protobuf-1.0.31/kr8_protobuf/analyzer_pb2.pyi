from google.protobuf import empty_pb2 as _empty_pb2
from kr8_protobuf import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Post(_message.Message):
    __slots__ = ("id", "approved")
    ID_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    id: str
    approved: bool
    def __init__(self, id: _Optional[str] = ..., approved: bool = ...) -> None: ...

class Posts(_message.Message):
    __slots__ = ("posts",)
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[Post]
    def __init__(self, posts: _Optional[_Iterable[_Union[Post, _Mapping]]] = ...) -> None: ...

class UserReport(_message.Message):
    __slots__ = ("user", "socialNetwork", "score", "post")
    USER_FIELD_NUMBER: _ClassVar[int]
    SOCIALNETWORK_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    user: str
    socialNetwork: str
    score: str
    post: str
    def __init__(self, user: _Optional[str] = ..., socialNetwork: _Optional[str] = ..., score: _Optional[str] = ..., post: _Optional[str] = ...) -> None: ...

class PostReport(_message.Message):
    __slots__ = ("report_likes", "report_comment", "positive_comment", "negative_comment")
    REPORT_LIKES_FIELD_NUMBER: _ClassVar[int]
    REPORT_COMMENT_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_COMMENT_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_COMMENT_FIELD_NUMBER: _ClassVar[int]
    report_likes: int
    report_comment: int
    positive_comment: int
    negative_comment: int
    def __init__(self, report_likes: _Optional[int] = ..., report_comment: _Optional[int] = ..., positive_comment: _Optional[int] = ..., negative_comment: _Optional[int] = ...) -> None: ...

class ChatRequest(_message.Message):
    __slots__ = ("body", "id", "post", "social_network")
    BODY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    SOCIAL_NETWORK_FIELD_NUMBER: _ClassVar[int]
    body: str
    id: str
    post: str
    social_network: str
    def __init__(self, body: _Optional[str] = ..., id: _Optional[str] = ..., post: _Optional[str] = ..., social_network: _Optional[str] = ...) -> None: ...
