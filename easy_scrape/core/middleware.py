from __future__ import annotations

from typing import Iterable, List

from .request import Request
from .response import Response


class BaseMiddleware:
    async def process_request(self, request: Request) -> Request:  # noqa: D401
        """Inspect/modify request before download."""
        return request

    async def process_response(self, request: Request, response: Response) -> Response:  # noqa: D401
        """Inspect/modify response after download."""
        return response


class MiddlewareManager:
    def __init__(self, middlewares: Iterable[BaseMiddleware] | None = None) -> None:
        self._middlewares: List[BaseMiddleware] = list(middlewares or [])

    @property
    def middlewares(self) -> List[BaseMiddleware]:
        return self._middlewares

    async def process_request(self, request: Request) -> Request:
        for m in self._middlewares:
            request = await m.process_request(request)
        return request

    async def process_response(self, request: Request, response: Response) -> Response:
        # Reverse order for response
        for m in reversed(self._middlewares):
            response = await m.process_response(request, response)
        return response

