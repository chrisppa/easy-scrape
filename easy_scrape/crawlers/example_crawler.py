from __future__ import annotations

from typing import Any, Iterable

from easy_scrape.core.crawler import Crawler
from easy_scrape.core.request import Request
from easy_scrape.core.response import Response


class ExampleCrawler(Crawler):
    name = "example"
    start_urls = [
        "https://example.org/",
    ]

    async def parse(self, response: Response) -> Iterable[Any]:
        title = response.css("title::text").get(default="").strip()
        links = [
            {
                "text": (a.css("::text").get(default="") or "").strip(),
                "href": a.attrib.get("href", ""),
            }
            for a in response.css("a")
        ]

        # Yield an item to pipelines
        yield {
            "url": response.url,
            "title": title,
            "links": links,
        }

        # Example of enqueueing a new request (disabled by default)
        # for a in response.css("a::attr(href)").getall():
        #     yield Request(response.urljoin(a), callback=self.parse)

