from __future__ import annotations

import asyncio
import inspect
from typing import Any, AsyncIterator, Awaitable, Iterable, List, Optional

from .browser import Browser
from .crawler import Crawler
from .downloader import Downloader
from .middleware import MiddlewareManager
from .pipeline import PipelineManager
from .request import Request
from .response import Response


class Runner:
    def __init__(
        self,
        *,
        concurrency: int = 10,
        middlewares: Optional[Iterable] = None,
        pipelines: Optional[Iterable] = None,
        request_timeout: float = 30.0,
    ) -> None:
        self.concurrency = max(1, concurrency)
        self.middleware = MiddlewareManager(middlewares)
        self.pipelines = PipelineManager(pipelines)
        self.request_timeout = request_timeout

        self._queue: asyncio.Queue[Request] = asyncio.Queue()

    async def run(self, crawler: Crawler) -> None:
        async with Downloader(timeout=self.request_timeout) as downloader:
            await self.pipelines.open()

            # Seed queue
            async for req in _ensure_async_iter(crawler.start_requests()):
                await self._queue.put(req)

            workers = [asyncio.create_task(self._worker(crawler, downloader)) for _ in range(self.concurrency)]

            await self._queue.join()

            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

            await self.pipelines.close()

    async def _worker(self, crawler: Crawler, downloader: Downloader) -> None:
        while True:
            request = await self._queue.get()
            try:
                request = await self.middleware.process_request(request)
                response: Response
                if request.use_browser:
                    # Use a short-lived browser context for now (simple stub)
                    async with Browser() as browser:
                        response = await browser.fetch(request)
                else:
                    response = await downloader.fetch(request)
                response = await self.middleware.process_response(request, response)

                callback = request.callback or getattr(crawler, "parse")
                async for output in _iterate_callback(callback, response):
                    if isinstance(output, Request):
                        await self._queue.put(output)
                    elif output is not None:
                        await self.pipelines.process_item(output, crawler)
            except Exception:  # pragma: no cover - basic debug
                # Minimal error reporting for early iteration
                import traceback

                traceback.print_exc()
            finally:
                self._queue.task_done()


async def _iterate_callback(func, response: Response) -> AsyncIterator[Any]:
    result = func(response)
    if inspect.isawaitable(result):
        result = await result

    # Async generator
    if inspect.isasyncgen(result):
        async for x in result:
            yield x
        return

    # Sync generator / iterable
    if inspect.isgenerator(result) or isinstance(result, (list, tuple, set)):
        for x in result:
            yield x
        return

    # Single item
    if result is not None:
        yield result


async def _ensure_async_iter(obj) -> AsyncIterator[Any]:
    if inspect.isasyncgen(obj):
        async for x in obj:
            yield x
        return
    if inspect.isawaitable(obj):
        obj = await obj
    if inspect.isgenerator(obj) or isinstance(obj, (list, tuple, set)):
        for x in obj:
            yield x
        return
    if obj is not None:
        yield obj

