Architecture

Core Components

- Request: carries URL, method, headers, params/data/json, meta, callback, and `use_browser`.
- Response: provides `url`, `status`, `text`/`content`, and Parsel selectors via `css()`/`xpath()`.
- Downloader: async HTTP client built on aiohttp.
- Browser: optional Playwright-based fetcher for JS-rendered pages, enabled per-request.
- MiddlewareManager: runs `process_request` (in order) and `process_response` (reverse order).
- PipelineManager: processes items through a chain of pipelines (`open`, `process_item`, `close`).
- Runner: asyncio task queue that seeds `start_requests`, downloads, dispatches callbacks, and handles outputs.

Flow

1) Seed: Crawler yields initial `Request`s from `start_requests()`
2) Queue: Runner enqueues requests and spins up workers
3) Request middlewares: modify/enrich request
4) Fetch: Downloader (or Browser) returns `Response`
5) Response middlewares: inspect/transform response
6) Callback: Crawler callback produces more `Request`s and/or items
7) Pipelines: items flow through pipelines for processing/export

Concurrency

- Configurable worker count via `Runner(concurrency=N)`
- Uses asyncio tasks; avoid blocking calls inside parse functions
