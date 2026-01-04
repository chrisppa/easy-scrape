from __future__ import annotations

from typing import Any, Iterable, List


class BasePipeline:
    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def process_item(self, item: Any, crawler: "Crawler") -> Any:  # noqa: F821
        return item


class PipelineManager:
    def __init__(self, pipelines: Iterable[BasePipeline] | None = None) -> None:
        self._pipelines: List[BasePipeline] = list(pipelines or [])

    async def open(self) -> None:
        for p in self._pipelines:
            await p.open()

    async def close(self) -> None:
        for p in reversed(self._pipelines):
            await p.close()

    async def process_item(self, item: Any, crawler: "Crawler") -> Any:  # noqa: F821
        for p in self._pipelines:
            item = await p.process_item(item, crawler)
        return item

