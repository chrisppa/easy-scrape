from __future__ import annotations

import json as _json
from typing import Any, Dict, Optional

from parsel import Selector


class Response:
    def __init__(
        self,
        *,
        url: str,
        status: int,
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        content: Optional[bytes] = None,
        request: Optional["Request"] = None,
    ) -> None:
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.text = text or (content.decode("utf-8", errors="replace") if content else "")
        self.content = content or self.text.encode("utf-8")
        self.request = request
        self._selector: Optional[Selector] = None

    # Selector helpers
    @property
    def selector(self) -> Selector:
        if self._selector is None:
            self._selector = Selector(text=self.text)
        return self._selector

    def css(self, query: str):
        return self.selector.css(query)

    def xpath(self, query: str):
        return self.selector.xpath(query)

    # Convenience
    def json(self) -> Any:
        return _json.loads(self.text)

    def __repr__(self) -> str:
        return f"Response(url={self.url!r}, status={self.status}, len={len(self.content)})"

