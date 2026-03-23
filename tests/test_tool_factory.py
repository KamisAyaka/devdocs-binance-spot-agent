from app.core.config import Settings
from app.tools.factory import create_tool_clients
from app.tools.web_fetch import WebFetchTool
from app.tools.web_search import DuckDuckGoSearchTool


def test_create_tool_clients_returns_expected_tools() -> None:
    settings = Settings(
        enable_web_search=True,
        enable_web_fetch=True,
        web_search_base_url="https://api.duckduckgo.com",
    )
    tools = create_tool_clients(settings)

    assert isinstance(tools["web_search"], DuckDuckGoSearchTool)
    assert isinstance(tools["web_fetch"], WebFetchTool)
