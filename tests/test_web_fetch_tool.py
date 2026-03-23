import httpx
import pytest

from app.core.exceptions import AppException
from app.tools.types import WebFetchRequest
from app.tools.web_fetch import WebFetchTool


@pytest.mark.asyncio
async def test_web_fetch_tool_success() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        html = """
        <html>
          <head><title>Binance Spot API</title></head>
          <body><h1>Docs</h1><p>Symbols endpoint details.</p></body>
        </html>
        """
        return httpx.Response(status_code=200, text=html)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        tool = WebFetchTool(timeout_s=3.0, max_chars=200, enabled=True, client=http_client)
        result = await tool.run(WebFetchRequest(url="https://example.com/doc"))

    assert result.tool_name == "web_fetch"
    assert result.success is True
    assert result.data["title"] == "Binance Spot API"
    assert "Symbols endpoint details." in result.data["content"]


@pytest.mark.asyncio
async def test_web_fetch_tool_http_error() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=404, text="not found")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        tool = WebFetchTool(timeout_s=3.0, max_chars=200, enabled=True, client=http_client)
        with pytest.raises(AppException) as exc_info:
            await tool.run(WebFetchRequest(url="https://example.com/missing"))

    assert exc_info.value.code == "TOOL_HTTP_ERROR"
