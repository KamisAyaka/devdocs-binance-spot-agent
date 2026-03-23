"""Application exception definitions and handlers."""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.schemas.common import ErrorDetail, ErrorResponse

logger = get_logger("errors")


class AppException(Exception):
    """Custom application exception."""

    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def register_exception_handlers(app: FastAPI) -> None:
    """Register centralized exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        request_id = _request_id(request)
        logger.warning(
            "app_exception",
            code=exc.code,
            message=exc.message,
            request_id=request_id,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=ErrorDetail(code=exc.code, message=exc.message, request_id=request_id),
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        request_id = _request_id(request)
        detail = str(exc.detail)
        logger.warning(
            "http_exception",
            status_code=exc.status_code,
            detail=detail,
            request_id=request_id,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=ErrorDetail(code="HTTP_ERROR", message=detail, request_id=request_id),
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = _request_id(request)
        logger.warning(
            "validation_exception",
            errors=exc.errors(),
            request_id=request_id,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=ErrorResponse(
                error=ErrorDetail(
                    code="VALIDATION_ERROR",
                    message="Request validation failed.",
                    request_id=request_id,
                ),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = _request_id(request)
        logger.exception(
            "unhandled_exception",
            request_id=request_id,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error=ErrorDetail(
                    code="INTERNAL_SERVER_ERROR",
                    message="Unexpected server error.",
                    request_id=request_id,
                ),
            ).model_dump(),
        )
