"""Web search tool client."""

from __future__ import annotations

from time import perf_counter

import httpx

from app.core.exceptions import AppException
from app.tools.base import ToolClient
from app.tools.types import SearchItem, ToolResult, WebSearchRequest


class DuckDuckGoSearchTool(ToolClient[WebSearchRequest]):
    """DuckDuckGo-based web search adapter."""

    name = "web_search"

    def __init__(
        self,
        *,
        base_url: str,
        timeout_s: float,
        enabled: bool,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.enabled = enabled
        self._client = client

    async def run(self, request: WebSearchRequest) -> ToolResult:
        if not self.enabled:
            raise AppException(
                code="TOOL_DISABLED",
                message="Web search tool is disabled.",
                status_code=400,
            )

        started = perf_counter()
        timeout = request.timeout_s or self.timeout_s
        params = {
            "q": request.query,
            "format": "json",
            "no_html": "1",
            "no_redirect": "1",
        }

        if self._client is not None:
            payload = await self._fetch(self._client, params, timeout)
        else:
            async with httpx.AsyncClient() as client:
                payload = await self._fetch(client, params, timeout)

        items = self._extract_items(payload, request.limit)
        latency_ms = round((perf_counter() - started) * 1000, 2)
        return ToolResult(
            tool_name=self.name,
            success=True,
            latency_ms=latency_ms,
            data={
                "query": request.query,
                "results": [item.model_dump() for item in items],
            },
        )

    async def _fetch(self, client: httpx.AsyncClient, params: dict[str, str], timeout: float) -> dict:
        try:
            response = await client.get(self.base_url, params=params, timeout=timeout)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise AppException(
                code="TOOL_TIMEOUT",
                message="Web search timed out.",
                status_code=504,
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise AppException(
                code="TOOL_HTTP_ERROR",
                message=f"Web search provider returned HTTP {exc.response.status_code}.",
                status_code=502,
            ) from exc
        except httpx.HTTPError as exc:
            raise AppException(
                code="TOOL_CONNECTION_ERROR",
                message="Web search provider connection failed.",
                status_code=502,
            ) from exc
        return response.json()

    def _extract_items(self, payload: dict, limit: int) -> list[SearchItem]:
        items: list[SearchItem] = []
        related_topics = payload.get("RelatedTopics") or []

        def append_item(title: str, url: str, snippet: str = "") -> None:
            if len(items) >= limit:
                return
            if not title or not url:
                return
            items.append(SearchItem(title=title, url=url, snippet=snippet))

        for item in related_topics:
            if len(items) >= limit:
                break
            if "Topics" in item:
                for nested in item.get("Topics", []):
                    append_item(
                        title=str(nested.get("Text", "")),
                        url=str(nested.get("FirstURL", "")),
                        snippet=str(nested.get("Text", "")),
                    )
                    if len(items) >= limit:
                        break
            else:
                append_item(
                    title=str(item.get("Text", "")),
                    url=str(item.get("FirstURL", "")),
                    snippet=str(item.get("Text", "")),
                )

        if not items:
            abstract_text = str(payload.get("AbstractText", ""))
            abstract_url = str(payload.get("AbstractURL", ""))
            append_item(title=abstract_text, url=abstract_url, snippet=abstract_text)
        return items
