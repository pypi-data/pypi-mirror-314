from __future__ import annotations

import sys
from typing import Any, Awaitable, Callable, Iterable, Literal, TypedDict, Union

if sys.version_info >= (3, 11):  # pragma: py-lt-311
    from typing import NotRequired
else:  # pragma: py-gte-311
    from typing_extensions import NotRequired


class ASGIVersions(TypedDict):
    spec_version: str
    version: Literal["2.0", "3.0"]


class HTTPScope(TypedDict):
    type: Literal["http"]
    asgi: ASGIVersions
    http_version: str
    method: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[tuple[bytes, bytes]]
    client: tuple[str, int] | None
    server: tuple[str, int | None] | None
    state: NotRequired[dict[str, Any]]
    extensions: NotRequired[dict[str, dict[object, object]]]


class WebSocketScope(TypedDict):
    type: Literal["websocket"]
    asgi: ASGIVersions
    http_version: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[tuple[bytes, bytes]]
    client: tuple[str, int] | None
    server: tuple[str, int | None] | None
    subprotocols: Iterable[str]
    state: NotRequired[dict[str, Any]]
    extensions: NotRequired[dict[str, dict[object, object]]]


class LifespanScope(TypedDict):
    type: Literal["lifespan"]
    asgi: ASGIVersions
    state: NotRequired[dict[str, Any]]


WWWScope = Union[HTTPScope, WebSocketScope]
Scope = Union[HTTPScope, WebSocketScope, LifespanScope]


class HTTPRequestEvent(TypedDict):
    type: Literal["http.request"]
    body: bytes
    more_body: bool


class HTTPResponseDebugEvent(TypedDict):
    type: Literal["http.response.debug"]
    info: dict[str, object]


class HTTPResponseStartEvent(TypedDict):
    type: Literal["http.response.start"]
    status: int
    headers: NotRequired[Iterable[tuple[bytes, bytes]]]
    trailers: NotRequired[bool]


class HTTPResponseBodyEvent(TypedDict):
    type: Literal["http.response.body"]
    body: bytes
    more_body: NotRequired[bool]


class HTTPResponseTrailersEvent(TypedDict):
    type: Literal["http.response.trailers"]
    headers: Iterable[tuple[bytes, bytes]]
    more_trailers: bool


class HTTPServerPushEvent(TypedDict):
    type: Literal["http.response.push"]
    path: str
    headers: Iterable[tuple[bytes, bytes]]


class HTTPDisconnectEvent(TypedDict):
    type: Literal["http.disconnect"]


class WebSocketConnectEvent(TypedDict):
    type: Literal["websocket.connect"]


class WebSocketAcceptEvent(TypedDict):
    type: Literal["websocket.accept"]
    subprotocol: NotRequired[str | None]
    headers: NotRequired[Iterable[tuple[bytes, bytes]]]


class _WebSocketReceiveEventBytes(TypedDict):
    type: Literal["websocket.receive"]
    bytes: bytes
    text: NotRequired[None]


class _WebSocketReceiveEventText(TypedDict):
    type: Literal["websocket.receive"]
    bytes: NotRequired[None]
    text: str


WebSocketReceiveEvent = Union[_WebSocketReceiveEventBytes, _WebSocketReceiveEventText]


class _WebSocketSendEventBytes(TypedDict):
    type: Literal["websocket.send"]
    bytes: bytes
    text: NotRequired[None]


class _WebSocketSendEventText(TypedDict):
    type: Literal["websocket.send"]
    bytes: NotRequired[None]
    text: str


WebSocketSendEvent = Union[_WebSocketSendEventBytes, _WebSocketSendEventText]


class WebSocketResponseStartEvent(TypedDict):
    type: Literal["websocket.http.response.start"]
    status: int
    headers: Iterable[tuple[bytes, bytes]]


class WebSocketResponseBodyEvent(TypedDict):
    type: Literal["websocket.http.response.body"]
    body: bytes
    more_body: NotRequired[bool]


class WebSocketDisconnectEvent(TypedDict):
    type: Literal["websocket.disconnect"]
    code: int
    reason: NotRequired[str | None]


class WebSocketCloseEvent(TypedDict):
    type: Literal["websocket.close"]
    code: NotRequired[int]
    reason: NotRequired[str | None]


class LifespanStartupEvent(TypedDict):
    type: Literal["lifespan.startup"]


class LifespanShutdownEvent(TypedDict):
    type: Literal["lifespan.shutdown"]


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal["lifespan.startup.complete"]


class LifespanStartupFailedEvent(TypedDict):
    type: Literal["lifespan.startup.failed"]
    message: str


class LifespanShutdownCompleteEvent(TypedDict):
    type: Literal["lifespan.shutdown.complete"]


class LifespanShutdownFailedEvent(TypedDict):
    type: Literal["lifespan.shutdown.failed"]
    message: str


WebSocketEvent = Union[WebSocketReceiveEvent, WebSocketDisconnectEvent, WebSocketConnectEvent]


ASGIReceiveEvent = Union[
    HTTPRequestEvent,
    HTTPDisconnectEvent,
    WebSocketConnectEvent,
    WebSocketReceiveEvent,
    WebSocketDisconnectEvent,
    LifespanStartupEvent,
    LifespanShutdownEvent,
]


ASGISendEvent = Union[
    HTTPResponseStartEvent,
    HTTPResponseBodyEvent,
    HTTPResponseTrailersEvent,
    HTTPServerPushEvent,
    HTTPDisconnectEvent,
    WebSocketAcceptEvent,
    WebSocketSendEvent,
    WebSocketResponseStartEvent,
    WebSocketResponseBodyEvent,
    WebSocketCloseEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
]


ASGIReceiveCallable = Callable[[], Awaitable[ASGIReceiveEvent]]
ASGISendCallable = Callable[[ASGISendEvent], Awaitable[None]]

ASGIApp = Callable[[Scope, ASGIReceiveCallable, ASGISendCallable], Awaitable[None]]
