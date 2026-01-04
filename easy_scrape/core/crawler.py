from __future__ import annotations

from typing import Iterable, List

from .request import Request


class Crawler:
    name: str = "crawler"
    start_urls: List[str] = []

    async def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    async def parse(self, response: "Response"):
        raise NotImplementedError("Crawler.parse must be implemented")

