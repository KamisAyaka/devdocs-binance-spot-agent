"""Application middlewares."""

from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request

from app.core.logging import get_logger

logger = get_logger("http")


def register_middlewares(app: FastAPI) -> None:
    """Register application middlewares."""

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        request.state.request_id = request_id

        start = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            latency_ms = round((perf_counter() - start) * 1000, 2)
            logger.exception(
                "request_failed",
                method=request.method,
                path=request.url.path,
                request_id=request_id,
                latency_ms=latency_ms,
            )
            raise

        latency_ms = round((perf_counter() - start) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-MS"] = str(latency_ms)

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            request_id=request_id,
            latency_ms=latency_ms,
        )
        return response
