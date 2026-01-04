from __future__ import annotations

from easy_scrape.core.middleware import BaseMiddleware
from easy_scrape.core.request import Request


class UserAgentMiddleware(BaseMiddleware):
    def __init__(self, user_agent: str | None = None) -> None:
        self.user_agent = user_agent or "easy-scrape/0.1 (+https://example.com)"

    async def process_request(self, request: Request) -> Request:
        headers = dict(request.headers or {})
        headers.setdefault("User-Agent", self.user_agent)
        request.headers = headers
        return request

