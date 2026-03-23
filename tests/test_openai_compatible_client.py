import httpx
import pytest

from app.core.exceptions import AppException
from app.models.openai_compatible import OpenAICompatibleModelClient
from app.models.types import ChatMessage, ModelRequest


@pytest.mark.asyncio
async def test_openai_compatible_client_generate_success() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        payload = {
            "id": "cmpl-test",
            "model": "gpt-4.1-mini",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "hello"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        return httpx.Response(status_code=200, json=payload)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = OpenAICompatibleModelClient(
            model="gpt-4.1-mini",
            api_key="test-key",
            base_url="https://example.com/v1",
            client=http_client,
        )
        response = await client.generate(
            ModelRequest(messages=[ChatMessage(role="user", content="hi")]),
        )

    assert response.text == "hello"
    assert response.model == "gpt-4.1-mini"
    assert response.finish_reason == "stop"
    assert response.usage.total_tokens == 15


@pytest.mark.asyncio
async def test_openai_compatible_client_generate_raises_on_http_error() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=500, json={"error": "bad upstream"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = OpenAICompatibleModelClient(
            model="gpt-4.1-mini",
            api_key="test-key",
            base_url="https://example.com/v1",
            client=http_client,
        )
        with pytest.raises(AppException) as exc_info:
            await client.generate(ModelRequest(messages=[ChatMessage(role="user", content="hi")]))

    assert exc_info.value.code == "MODEL_HTTP_ERROR"
