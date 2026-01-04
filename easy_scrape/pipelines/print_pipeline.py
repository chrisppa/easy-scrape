from __future__ import annotations

import json
from typing import Any

from easy_scrape.core.pipeline import BasePipeline


class PrintPipeline(BasePipeline):
    async def process_item(self, item: Any, crawler) -> Any:
        try:
            print(json.dumps(item, ensure_ascii=False, indent=2))
        except Exception:
            print(item)
        return item

