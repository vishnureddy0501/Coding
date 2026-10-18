import os
from dataclasses import dataclass

from dotenv import load_dotenv


# Reads .env during local development.
# Existing environment variables are not overwritten.
load_dotenv()


def read_boolean(name: str, default: bool = False) -> bool:
    value = os.getenv(name, str(default))
    return value.lower() in {"true", "1", "yes"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_environment: str
    debug: bool
    welcome_message: str
    demo_secret: str


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "FastAPI Docker Demo"),
        app_environment=os.getenv("APP_ENV", "development"),
        debug=read_boolean("DEBUG"),
        welcome_message=os.getenv("WELCOME_MESSAGE", "Hello from FastAPI"),
        demo_secret=os.getenv("DEMO_SECRET", "not-configured"),
    )


settings = get_settings()
