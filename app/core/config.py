"""Application configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DEVDOCS_",
        extra="ignore",
    )

    app_name: str = "DevDocs Binance Spot Agent"
    app_version: str = "0.1.0"
    app_env: Literal["local", "test", "prod"] = "local"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    model_provider: str = "openai-compatible"
    model_name: str = "gpt-4.1-mini"
    model_base_url: AnyHttpUrl | None = None
    model_api_key: str | None = Field(default=None, repr=False)

    database_url: str = "sqlite:///./devdocs.db"
    enable_web_search: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
