"""Configuration response schemas."""

from typing import Literal

from pydantic import BaseModel


class ConfigPayload(BaseModel):
    """Safe runtime configuration summary."""

    app_name: str
    app_version: str
    app_env: Literal["local", "test", "prod"]
    debug: bool
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    model_provider: str
    model_name: str
    model_base_url: str | None
    database_url: str
    enable_web_search: bool
