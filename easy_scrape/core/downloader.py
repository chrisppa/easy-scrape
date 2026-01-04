from __future__ import annotations

from typing import Optional

import aiohttp

from .request import Request
from .response import Response


class Downloader:
    def __init__(self, *, timeout: float = 30.0, default_headers: Optional[dict] = None) -> None:
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._default_headers = default_headers or {}
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "Downloader":
        self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def fetch(self, request: Request) -> Response:
        assert self._session is not None, "Downloader session not started"
        headers = {**self._default_headers, **(request.headers or {})}
        async with self._session.request(
            request.method,
            request.url,
            headers=headers,
            params=request.params,
            data=request.data,
            json=request.json,
        ) as resp:
            content = await resp.read()
            return Response(
                url=str(resp.url),
                status=resp.status,
                headers={k: v for k, v in resp.headers.items()},
                content=content,
                request=request,
            )

