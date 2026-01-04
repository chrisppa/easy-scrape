easy-scrape (Starter)

A minimal, async-first scraping framework skeleton built on Python’s asyncio. It favors simplicity and quick experimentation while keeping familiar concepts: crawlers, middlewares, and pipelines. Static pages use aiohttp + Parsel; dynamic pages can opt into Playwright. The goal of easy-scrape is simple: make scraping easy.

Quick Start

- Python: 3.10+
- Create and activate a virtual environment (recommended):
  - Unix/macOS: `python3 -m venv .venv && source .venv/bin/activate`
  - Windows (PowerShell): `py -m venv .venv; .venv\\Scripts\\Activate.ps1`
- Install deps inside the venv: `pip install -r requirements.txt`
- (Optional for dynamic sites inside the venv) `pip install playwright` then `python -m playwright install chromium`
- Run the example crawler with CLI (inside the venv):
  - `python -m easy_scrape.cli run easy_scrape.crawlers.example_crawler:ExampleCrawler`

Contributing and Community

- Contributions are welcome! See `CONTRIBUTING.md` for guidelines.
- Please follow our `CODE_OF_CONDUCT.md`.
- Security issues? See `SECURITY.md` for private reporting instructions.

License

This project is licensed under the MIT License — see `LICENSE` for details.

Project Structure

- `easy_scrape/core/` – engine, request/response, downloader, browser stub
- `easy_scrape/crawlers/` – crawlers (site-specific logic)
- `easy_scrape/middlewares/` – request/response middlewares
- `easy_scrape/pipelines/` – item pipelines
- `easy_scrape/cli.py` – simple CLI entry to run crawlers
- `examples/run_example.py` – example runner

Design Choices

- HTTP: aiohttp (async, efficient, simple). HTTPX is available if you prefer.
- Selectors: Parsel (CSS/XPath) backed by lxml.
- Dynamic: Playwright provided via optional stub; enable per-request with `use_browser=True`.
- Concurrency: asyncio with a task queue and configurable concurrency.

Usage Notes

- Write crawlers by subclassing `Crawler` and implementing `parse(self, response)`.
- Yield `Request` objects for follow-up pages and dict-like items for pipelines.
- Configure middlewares/pipelines in the CLI or your own runner.
