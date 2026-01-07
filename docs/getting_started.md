Getting Started

Overview

- Purpose: Async-first, lightweight scraping with crawlers, middlewares, and pipelines.
- HTTP: aiohttp (static pages), selectors via Parsel (CSS/XPath).
- Dynamic pages: Playwright via `use_browser=True` per request (optional install).

Prerequisites

- Python 3.10+
- Recommended: a virtual environment

Setup

- macOS/Linux:
  - `python3 -m venv .venv && source .venv/bin/activate`
- Windows (PowerShell):
  - `py -m venv .venv; .venv\\Scripts\\Activate.ps1`
- Install dependencies:
  - `pip install -r requirements.txt`
- (Optional) Dynamic pages:
  - `pip install playwright`
  - `python -m playwright install chromium`

Run the Example Crawler

- Show CLI help:
  - `python -m easy_scrape.cli -h`
- Run the example:
  - `python -m easy_scrape.cli run easy_scrape.crawlers.example_crawler:ExampleCrawler`
- Override start URL and concurrency:
  - `python -m easy_scrape.cli run easy_scrape.crawlers.example_crawler:ExampleCrawler -u https://example.org/ -c 20`

Programmatic Runner

```
import asyncio
from easy_scrape.core.runner import Runner
from easy_scrape.crawlers.example_crawler import ExampleCrawler
from easy_scrape.middlewares.user_agent import UserAgentMiddleware
from easy_scrape.pipelines.print_pipeline import PrintPipeline

async def main():
    runner = Runner(concurrency=10, middlewares=[UserAgentMiddleware()], pipelines=[PrintPipeline()])
    await runner.run(ExampleCrawler())

if __name__ == "__main__":
    asyncio.run(main())
```

Next Steps

- Write your first crawler (see crawlers.md)
- Explore middlewares/pipelines (see middlewares_pipelines.md)
- Check experiments and troubleshooting for tips
