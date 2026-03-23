"""Shared response schemas."""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class SuccessResponse(BaseModel, Generic[DataT]):
    """Standard success response envelope."""

    success: bool = True
    message: str = "ok"
    data: DataT


class HealthPayload(BaseModel):
    """Health check payload."""

    status: str = Field(default="ok")
    service: str
