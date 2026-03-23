from app.core.config import Settings


def test_settings_can_be_loaded_from_values() -> None:
    settings = Settings(
        app_env="test",
        log_level="DEBUG",
        model_name="test-model",
        database_url="sqlite:///./test.db",
        enable_web_search=True,
    )

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.model_name == "test-model"
    assert settings.database_url == "sqlite:///./test.db"
    assert settings.enable_web_search is True
