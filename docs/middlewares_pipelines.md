Middlewares & Pipelines

Middlewares

- Purpose: modify requests (headers, proxies, retries) and responses (logging, transforms)
- Base class: `BaseMiddleware`
- Methods:
  - `async def process_request(self, request) -> Request`
  - `async def process_response(self, request, response) -> Response`

Example Middleware

```
from easy_scrape.core.middleware import BaseMiddleware

class HeaderMiddleware(BaseMiddleware):
    def __init__(self, header_value: str):
        self.header_value = header_value

    async def process_request(self, request):
        headers = dict(request.headers or {})
        headers["X-My-Header"] = self.header_value
        request.headers = headers
        return request
```

Pipelines

- Purpose: process/export items (cleaning, validation, JSON/CSV, DB)
- Base class: `BasePipeline`
- Methods: `open()`, `process_item(item, crawler)`, `close()`

Example Pipeline

```
import json
from easy_scrape.core.pipeline import BasePipeline

class JsonLinesPipeline(BasePipeline):
    def __init__(self, path="items.jl"):
        self.path = path
        self.f = None

    async def open(self):
        self.f = open(self.path, "a", encoding="utf-8")

    async def close(self):
        if self.f:
            self.f.close()

    async def process_item(self, item, crawler):
        self.f.write(json.dumps(item, ensure_ascii=False) + "\n")
        return item
```

Wiring Them Up

- Programmatically via Runner:

```
from easy_scrape.core.runner import Runner
runner = Runner(concurrency=10, middlewares=[HeaderMiddleware("value")], pipelines=[JsonLinesPipeline("out.jl")])
```

- CLI currently uses built-in defaults (UserAgentMiddleware, PrintPipeline). Extend via your own runner script.
