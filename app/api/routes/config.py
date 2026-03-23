"""Configuration routes."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.common import SuccessResponse
from app.schemas.config import ConfigPayload

router = APIRouter()


@router.get("/config", response_model=SuccessResponse[ConfigPayload])
async def get_runtime_config(
    settings: Settings = Depends(get_settings),
) -> SuccessResponse[ConfigPayload]:
    """Return a safe summary of the current runtime configuration."""
    return SuccessResponse(
        message="Runtime config loaded.",
        data=ConfigPayload(
            app_name=settings.app_name,
            app_version=settings.app_version,
            app_env=settings.app_env,
            debug=settings.debug,
            log_level=settings.log_level,
            model_provider=settings.model_provider,
            model_name=settings.model_name,
            model_base_url=str(settings.model_base_url) if settings.model_base_url else None,
            database_url=settings.database_url,
            enable_web_search=settings.enable_web_search,
        ),
    )
