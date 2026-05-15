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

    # -------------------
    # DATABASE
    # -------------------
    DATABASE_URL: str



settings = Settings()