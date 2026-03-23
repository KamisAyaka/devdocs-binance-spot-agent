"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import register_middlewares


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Developer-facing agent service for Binance Spot API documentation.",
        debug=settings.debug,
    )
    register_middlewares(app)
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
