"""Web content fetch tool client."""

from __future__ import annotations

import re
from html import unescape
from time import perf_counter

import httpx

from app.core.exceptions import AppException
from app.tools.base import ToolClient
from app.tools.types import ToolResult, WebFetchRequest


_TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_SCRIPT_STYLE_PATTERN = re.compile(r"<(script|style)[^>]*>.*?</\\1>", re.IGNORECASE | re.DOTALL)
_TAG_PATTERN = re.compile(r"<[^>]+>")
_WS_PATTERN = re.compile(r"\s+")


class WebFetchTool(ToolClient[WebFetchRequest]):
    """HTTP page fetch adapter."""

    name = "web_fetch"

    def __init__(
        self,
        *,
        timeout_s: float,
        max_chars: int,
        enabled: bool,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.timeout_s = timeout_s
        self.max_chars = max_chars
        self.enabled = enabled
        self._client = client

    async def run(self, request: WebFetchRequest) -> ToolResult:
        if not self.enabled:
            raise AppException(
                code="TOOL_DISABLED",
                message="Web fetch tool is disabled.",
                status_code=400,
            )

        started = perf_counter()
        timeout = request.timeout_s or self.timeout_s

        if self._client is not None:
            response = await self._fetch(self._client, request.url, timeout)
        else:
            async with httpx.AsyncClient() as client:
                response = await self._fetch(client, request.url, timeout)

        title = self._extract_title(response.text)
        text = self._extract_text(response.text, self.max_chars)
        latency_ms = round((perf_counter() - started) * 1000, 2)
        return ToolResult(
            tool_name=self.name,
            success=True,
            latency_ms=latency_ms,
            data={
                "url": request.url,
                "status_code": response.status_code,
                "title": title,
                "content": text,
            },
        )

    async def _fetch(self, client: httpx.AsyncClient, url: str, timeout: float) -> httpx.Response:
        try:
            response = await client.get(url, timeout=timeout)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise AppException(
                code="TOOL_TIMEOUT",
                message="Web fetch timed out.",
                status_code=504,
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise AppException(
                code="TOOL_HTTP_ERROR",
                message=f"Web fetch returned HTTP {exc.response.status_code}.",
                status_code=502,
            ) from exc
        except httpx.HTTPError as exc:
            raise AppException(
                code="TOOL_CONNECTION_ERROR",
                message="Web fetch connection failed.",
                status_code=502,
            ) from exc
        return response

    def _extract_title(self, html: str) -> str:
        match = _TITLE_PATTERN.search(html)
        if not match:
            return ""
        return _WS_PATTERN.sub(" ", unescape(match.group(1))).strip()

    def _extract_text(self, html: str, max_chars: int) -> str:
        cleaned = _SCRIPT_STYLE_PATTERN.sub(" ", html)
        cleaned = _TAG_PATTERN.sub(" ", cleaned)
        cleaned = _WS_PATTERN.sub(" ", unescape(cleaned)).strip()
        return cleaned[:max_chars]
