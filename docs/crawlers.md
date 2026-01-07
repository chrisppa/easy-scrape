Writing Crawlers

Basics

- Subclass `Crawler` and implement `parse(self, response)`
- Define `start_urls` or override `start_requests()`
- Yield `Request` for follow-up pages; yield dict-like items for pipelines

Example

```
from urllib.parse import urljoin
from easy_scrape.core.crawler import Crawler
from easy_scrape.core.request import Request

class QuotesCrawler(Crawler):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    async def parse(self, response):
        for q in response.css(".quote"):
            yield {
                "text": q.css(".text::text").get(),
                "author": q.css(".author::text").get(),
            }
        next_href = response.css("li.next a::attr(href)").get()
        if next_href:
            yield Request(urljoin(response.url, next_href), callback=self.parse)
```

Selectors Cheat Sheet

- Text: `response.css("h1::text").get()`; all: `.getall()`
- Attr: `response.css("a::attr(href)").getall()`
- XPath: `response.xpath("//h1/text()").get()`
- JSON: `response.json()` for API responses

Dynamic Pages

- Install Playwright and Chromium
- For a specific request: `Request("https://site", use_browser=True, callback=self.parse)`

Tips

- Keep parsing non-blocking; use async where needed
- Store context in `request.meta` if you need to pass state
