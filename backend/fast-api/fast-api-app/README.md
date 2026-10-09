# FastAPI application

Minimal FastAPI setup with a separate asynchronous MongoDB connection module.

## Structure

```text
fast-api-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── .env
├── .gitignore
├── pyproject.toml
└── uv.lock
```

## Environment

The local `.env` file contains:

```text
FASTAPI_PRACTICE_APP_NAME
FASTAPI_PRACTICE_APP_ENV
FASTAPI_PRACTICE_DEBUG
MONGO_URL
MONGO_DATABASE
```

Keep `.env` out of Git. Use a real secret manager in production.

## Install

```bash
uv sync
```

## Run

Start MongoDB locally, then run:

```bash
uv run fastapi dev app/main.py
```

Open:

- Swagger: `http://127.0.0.1:8000/swagger`
- Health: `http://127.0.0.1:8000/health`

The application verifies MongoDB during startup. If MongoDB is unavailable, startup fails instead of accepting requests without a database connection.
