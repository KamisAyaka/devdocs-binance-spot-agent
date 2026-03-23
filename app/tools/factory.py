"""Factory for tool clients."""

from typing import Any

from app.core.config import Settings
from app.tools.base import ToolClient
from app.tools.web_fetch import WebFetchTool
from app.tools.web_search import DuckDuckGoSearchTool


def create_tool_clients(settings: Settings) -> dict[str, ToolClient[Any]]:
    """Build all default tool clients from runtime settings."""
    return {
        "web_search": DuckDuckGoSearchTool(
            base_url=str(settings.web_search_base_url),
            timeout_s=settings.web_search_timeout_s,
            enabled=settings.enable_web_search,
        ),
        "web_fetch": WebFetchTool(
            timeout_s=settings.web_fetch_timeout_s,
            max_chars=settings.web_fetch_max_chars,
            enabled=settings.enable_web_fetch,
        ),
    }
