from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


CallbackType = Optional[Callable[["Response"], Any]]


@dataclass
class Request:
    url: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    data: Any = None
    json: Any = None
    meta: Dict[str, Any] = field(default_factory=dict)
    use_browser: bool = False
    callback: CallbackType = None

    def replace(self, **kwargs) -> "Request":
        data = self.__dict__.copy()
        data.update(kwargs)
        return Request(**data)

