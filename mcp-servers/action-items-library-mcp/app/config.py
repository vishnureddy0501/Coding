from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongo_uri: str = Field(validation_alias="MONGO_URI")
    mongo_database: str = Field(validation_alias="MONGO_DATABASE")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
