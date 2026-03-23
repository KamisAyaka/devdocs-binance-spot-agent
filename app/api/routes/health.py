"""Health check routes."""

from fastapi import APIRouter

from app.schemas.common import HealthPayload, SuccessResponse

router = APIRouter()


@router.get("/health", response_model=SuccessResponse[HealthPayload])
async def health_check() -> SuccessResponse[HealthPayload]:
    """Basic health endpoint for service availability checks."""
    return SuccessResponse(
        message="Service is healthy.",
        data=HealthPayload(status="ok", service="devdocs-binance-spot-agent"),
    )
