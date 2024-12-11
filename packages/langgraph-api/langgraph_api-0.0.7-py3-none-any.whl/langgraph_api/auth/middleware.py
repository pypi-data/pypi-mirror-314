from starlette.middleware import Middleware
from starlette.middleware.authentication import (
    AuthenticationError,
    AuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

from langgraph_api.config import LANGGRAPH_AUTH_TYPE


def get_auth_backend():
    if LANGGRAPH_AUTH_TYPE == "langsmith":
        from langgraph_api.auth.langsmith.backend import LangsmithAuthBackend

        return LangsmithAuthBackend()
    else:
        from langgraph_api.auth.noop import NoopAuthBackend

        return NoopAuthBackend()


def on_error(conn: HTTPConnection, exc: AuthenticationError):
    return JSONResponse({"detail": str(exc)}, status_code=403)


class ConditionalAuthenticationMiddleware(AuthenticationMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["root_path"] == "/noauth":
            # disable auth for requests originating from SDK ASGI transport
            # root_path cannot be set from a request, so safe to use as auth bypass
            await self.app(scope, receive, send)
            return

        return await super().__call__(scope, receive, send)


auth_middleware = Middleware(
    ConditionalAuthenticationMiddleware, backend=get_auth_backend(), on_error=on_error
)
