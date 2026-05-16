from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------
    # APP CONFIG
    # -------------------
    APP_NAME: str = "Unified Payment Gateway"
    DEBUG: bool = False
    ENV: str = "development"
    SENTRY_DSN: str | None = None
    SENTRY_ENVIRONMENT: str | None = None
    SENTRY_RELEASE: str | None = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.0
    SENTRY_PROFILES_SAMPLE_RATE: float = 0.0

    # -------------------
    # DATABASE
    # -------------------
    DATABASE_URL: str



settings = Settings()