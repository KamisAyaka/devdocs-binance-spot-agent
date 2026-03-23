"""Factory methods for model clients."""

from app.core.config import Settings
from app.core.exceptions import AppException
from app.models.base import ModelClient
from app.models.openai_compatible import OpenAICompatibleModelClient


def create_model_client(settings: Settings) -> ModelClient:
    """Build a model client from runtime settings."""
    provider = settings.model_provider.strip().lower()
    if provider != "openai-compatible":
        raise AppException(
            code="UNSUPPORTED_MODEL_PROVIDER",
            message=f"Unsupported model provider: {settings.model_provider}.",
            status_code=500,
        )

    if not settings.model_api_key:
        raise AppException(
            code="MODEL_CONFIG_ERROR",
            message="Missing model API key configuration.",
            status_code=500,
        )

    if not settings.model_base_url:
        raise AppException(
            code="MODEL_CONFIG_ERROR",
            message="Missing model base URL configuration.",
            status_code=500,
        )

    return OpenAICompatibleModelClient(
        model=settings.model_name,
        api_key=settings.model_api_key,
        base_url=str(settings.model_base_url),
    )
