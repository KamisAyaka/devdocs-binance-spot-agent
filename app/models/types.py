"""Shared model-layer types."""

from typing import Literal

from pydantic import BaseModel, Field


Role = Literal["system", "user", "assistant", "tool"]


class ChatMessage(BaseModel):
    """Normalized chat message."""

    role: Role
    content: str


class ModelRequest(BaseModel):
    """Unified model request payload."""

    messages: list[ChatMessage]
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1)
    timeout_s: float = Field(default=30.0, gt=0.0)


class ModelUsage(BaseModel):
    """Token usage summary."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ModelResponse(BaseModel):
    """Unified model response payload."""

    text: str
    model: str
    finish_reason: str | None = None
    usage: ModelUsage = Field(default_factory=ModelUsage)
    raw: dict | None = None
