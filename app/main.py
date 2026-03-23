"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.router import api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="DevDocs Binance Spot Agent",
        version="0.1.0",
        description="Developer-facing agent service for Binance Spot API documentation.",
    )
    app.include_router(api_router)
    return app


app = create_app()
