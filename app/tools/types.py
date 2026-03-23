"""Shared tool-layer types."""

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """Unified tool execution result."""

    tool_name: str
    success: bool
    latency_ms: float = Field(ge=0.0)
    data: dict


class WebSearchRequest(BaseModel):
    """Web search request."""

    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=10)
    timeout_s: float | None = Field(default=None, gt=0.0)


class SearchItem(BaseModel):
    """Normalized search result item."""

    title: str
    url: str
    snippet: str = ""


class WebFetchRequest(BaseModel):
    """Web fetch request."""

    url: str
    timeout_s: float | None = Field(default=None, gt=0.0)

