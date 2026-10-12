from functools import lru_cache
from typing import Literal

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
    app_env: Literal["development", "production"] = Field(
        default="development",
        validation_alias="FASTAPI_PRACTICE_APP_ENV",
    )
    debug: bool = Field(
        default=False,
        validation_alias="FASTAPI_PRACTICE_DEBUG",
    )
    mongo_url: str = Field(
        default="",
        validation_alias="MONGO_URL",
    )
    mongo_database: str = Field(
        default="",
        validation_alias="MONGO_DATABASE",
    )
    def validate_runtime(self) -> None:
        missing: list[str] = []
        if not self.mongo_url:
            missing.append("MONGO_URL")
        if not self.mongo_database:
            missing.append("MONGO_DATABASE")
        if missing:
            names = ", ".join(missing)
            raise RuntimeError(f"Missing required environment variables: {names}")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
