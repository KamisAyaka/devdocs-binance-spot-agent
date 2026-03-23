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
    web_search_provider: str
    web_search_base_url: str
    web_search_timeout_s: float
    enable_web_fetch: bool
    web_fetch_timeout_s: float
    web_fetch_max_chars: int
