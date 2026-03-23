import httpx
import pytest

from app.core.exceptions import AppException
from app.tools.types import WebSearchRequest
from app.tools.web_search import DuckDuckGoSearchTool


@pytest.mark.asyncio
async def test_web_search_tool_success() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["q"] == "binance spot api"
        payload = {
            "RelatedTopics": [
                {"Text": "Binance Spot API Docs", "FirstURL": "https://example.com/docs"},
                {"Text": "Rate Limits", "FirstURL": "https://example.com/limits"},
            ]
        }
        return httpx.Response(status_code=200, json=payload)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        tool = DuckDuckGoSearchTool(
            base_url="https://example.com/search",
            timeout_s=3.0,
            enabled=True,
            client=http_client,
        )
        result = await tool.run(WebSearchRequest(query="binance spot api", limit=2))

    assert result.tool_name == "web_search"
    assert result.success is True
    assert len(result.data["results"]) == 2
    assert result.data["results"][0]["title"] == "Binance Spot API Docs"


@pytest.mark.asyncio
async def test_web_search_tool_disabled() -> None:
    tool = DuckDuckGoSearchTool(
        base_url="https://example.com/search",
        timeout_s=3.0,
        enabled=False,
    )
    with pytest.raises(AppException) as exc_info:
        await tool.run(WebSearchRequest(query="binance"))

    assert exc_info.value.code == "TOOL_DISABLED"
