from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(
        default="FastAPI Application",
        validation_alias="FASTAPI_PRACTICE_APP_NAME",
    )
    app_env: str = Field(
        default="development",
        validation_alias="FASTAPI_PRACTICE_APP_ENV",
    )
    debug: bool = Field(
        default=False,
        validation_alias="FASTAPI_PRACTICE_DEBUG",
    )
    mongo_url: str = Field(
        default="mongodb://localhost:27017",
        validation_alias="MONGO_URL",
    )
    mongo_database: str = Field(
        default="fastapi_app",
        validation_alias="MONGO_DATABASE",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
