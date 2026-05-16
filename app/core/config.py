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
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800


    # -------------------
    # WEBHOOK
    # -------------------
    WEBHOOK_SECRET: str

    SECRET_KEY: str
    WEBHOOK_SECRET: str

    LOG_LEVEL: str = "INFO"



settings = Settings()