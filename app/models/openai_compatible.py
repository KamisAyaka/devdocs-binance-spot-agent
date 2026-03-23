"""OpenAI-compatible model client."""

from __future__ import annotations

from typing import Any

import httpx

from app.core.exceptions import AppException
from app.models.base import ModelClient
from app.models.types import ModelRequest, ModelResponse, ModelUsage


class OpenAICompatibleModelClient(ModelClient):
    """Adapter for OpenAI-compatible chat completion endpoints."""

    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        base_url: str,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = client

    async def generate(self, request: ModelRequest) -> ModelResponse:
        payload = {
            "model": self.model,
            "messages": [message.model_dump() for message in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if self._client is not None:
            return await self._send(self._client, headers, payload, request.timeout_s)

        async with httpx.AsyncClient() as client:
            return await self._send(client, headers, payload, request.timeout_s)

    async def _send(
        self,
        client: httpx.AsyncClient,
        headers: dict[str, str],
        payload: dict[str, Any],
        timeout_s: float,
    ) -> ModelResponse:
        url = f"{self.base_url}/chat/completions"
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=timeout_s)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise AppException(
                code="MODEL_TIMEOUT",
                message="Model request timed out.",
                status_code=504,
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise AppException(
                code="MODEL_HTTP_ERROR",
                message=f"Model provider returned HTTP {exc.response.status_code}.",
                status_code=502,
            ) from exc
        except httpx.HTTPError as exc:
            raise AppException(
                code="MODEL_CONNECTION_ERROR",
                message="Model provider connection failed.",
                status_code=502,
            ) from exc

        body = response.json()
        choices = body.get("choices") or []
        if not choices:
            raise AppException(
                code="MODEL_INVALID_RESPONSE",
                message="Model provider response missing choices.",
                status_code=502,
            )

        first_choice = choices[0]
        message = first_choice.get("message") or {}
        text = message.get("content")
        if not isinstance(text, str):
            raise AppException(
                code="MODEL_INVALID_RESPONSE",
                message="Model provider response missing text content.",
                status_code=502,
            )

        usage_data = body.get("usage") or {}
        usage = ModelUsage(
            prompt_tokens=int(usage_data.get("prompt_tokens", 0) or 0),
            completion_tokens=int(usage_data.get("completion_tokens", 0) or 0),
            total_tokens=int(usage_data.get("total_tokens", 0) or 0),
        )

        return ModelResponse(
            text=text,
            model=str(body.get("model") or self.model),
            finish_reason=first_choice.get("finish_reason"),
            usage=usage,
            raw=body,
        )
