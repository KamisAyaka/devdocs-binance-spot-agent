"""Model client abstraction."""

from abc import ABC, abstractmethod

from app.models.types import ModelRequest, ModelResponse


class ModelClient(ABC):
    """Base interface for all model providers."""

    @abstractmethod
    async def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate completion from input messages."""
