"""Tool client abstraction."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.tools.types import ToolResult

RequestT = TypeVar("RequestT")


class ToolClient(ABC, Generic[RequestT]):
    """Base interface for all tools."""

    name: str

    @abstractmethod
    async def run(self, request: RequestT) -> ToolResult:
        """Execute tool request."""
