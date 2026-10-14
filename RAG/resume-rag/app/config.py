from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Configuration that can be overridden from a local .env file."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = ""
    cloudinary_url: str = ""
    gemini_api_key: str = ""
    gemini_embedding_model: str = "gemini-embedding-001"
    gemini_chat_model: str = "gemini-3.1-flash-lite"
    max_upload_mb: int = Field(default=5, ge=1, le=25)
    top_k: int = Field(default=5, ge=1, le=15)

    @property
    def async_database_url(self) -> str:
        """Convert Neon's standard Postgres URL for SQLAlchemy's async driver."""
        url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Neon provides libpq-style parameters. asyncpg uses `ssl` instead and
        # does not accept the optional libpq `channel_binding` parameter.
        return (
            url.replace("sslmode=require", "ssl=require")
            .replace("&channel_binding=require", "")
            .replace("channel_binding=require&", "")
        )

    def validate_runtime(self) -> None:
        missing = [
            name
            for name, value in {
                "DATABASE_URL": self.database_url,
                "CLOUDINARY_URL": self.cloudinary_url,
                "GEMINI_API_KEY": self.gemini_api_key,
            }.items()
            if not value
        ]
        if missing:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
