from __future__ import annotations

import asyncio
import typing

AutoWebSocketsProtocol: typing.Callable[..., asyncio.Protocol] | None
try:
    import websockets  # noqa
except ImportError:  # pragma: no cover
    try:
        import wsproto  # noqa
    except ImportError:
        AutoWebSocketsProtocol = None
    else:
        from forgeserver.protocols.websockets.wsproto_impl import WSProtocol

        AutoWebSocketsProtocol = WSProtocol
else:
    from forgeserver.protocols.websockets.websockets_impl import WebSocketProtocol

    AutoWebSocketsProtocol = WebSocketProtocol
