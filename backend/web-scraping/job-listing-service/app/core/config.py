from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str
    kafka_bootstrap_servers: str
    kafka_job_topic: str = "jobs.normalized.v1"
    kafka_consumer_group: str = "job-listing-worker-v1"
    naukri_mode: str = "sample"
    naukri_search_url_template: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
