from __future__ import annotations

from typing import Optional

from .request import Request
from .response import Response


class Browser:
    """Optional Playwright-based fetcher for dynamic pages.

    Lazily imports Playwright. If Playwright is not installed, using this
    will raise a RuntimeError with an installation hint.
    """

    def __init__(self, *, headless: bool = True):
        self._playwright = None
        self._browser = None
        self._context = None
        self._headless = headless

    async def __aenter__(self) -> "Browser":
        try:
            from playwright.async_api import async_playwright  # type: ignore
        except Exception as e:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "Playwright is not installed. Install with 'pip install playwright' and 'python -m playwright install chromium'"
            ) from e

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self._headless)
        self._context = await self._browser.new_context()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._context is not None:
            await self._context.close()
        if self._browser is not None:
            await self._browser.close()
        if self._playwright is not None:
            await self._playwright.stop()
        self._context = None
        self._browser = None
        self._playwright = None

    async def fetch(self, request: Request) -> Response:
        assert self._context is not None, "Browser is not started"
        page = await self._context.new_page()
        # Basic headers support via context options can be added later.
        resp = await page.goto(request.url, wait_until="networkidle")
        html = await page.content()
        status = resp.status if resp else 200
        await page.close()
        return Response(url=request.url, status=status, text=html, request=request)

