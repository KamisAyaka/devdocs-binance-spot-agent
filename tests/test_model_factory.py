import pytest

from app.core.config import Settings
from app.core.exceptions import AppException
from app.models.factory import create_model_client
from app.models.openai_compatible import OpenAICompatibleModelClient


def test_create_model_client_returns_openai_compatible_client() -> None:
    settings = Settings(
        model_provider="openai-compatible",
        model_name="gpt-4.1-mini",
        model_api_key="test-key",
        model_base_url="https://api.openai.com/v1",
    )

    client = create_model_client(settings)

    assert isinstance(client, OpenAICompatibleModelClient)


def test_create_model_client_raises_for_unsupported_provider() -> None:
    settings = Settings(model_provider="anthropic")

    with pytest.raises(AppException) as exc_info:
        create_model_client(settings)

    assert exc_info.value.code == "UNSUPPORTED_MODEL_PROVIDER"


def test_create_model_client_raises_when_api_key_missing() -> None:
    settings = Settings(
        model_provider="openai-compatible",
        model_base_url="https://api.openai.com/v1",
        model_api_key=None,
    )

    with pytest.raises(AppException) as exc_info:
        create_model_client(settings)

    assert exc_info.value.code == "MODEL_CONFIG_ERROR"


def test_create_model_client_raises_when_base_url_missing() -> None:
    settings = Settings(
        model_provider="openai-compatible",
        model_api_key="test-key",
        model_base_url=None,
    )

    with pytest.raises(AppException) as exc_info:
        create_model_client(settings)

    assert exc_info.value.code == "MODEL_CONFIG_ERROR"
