# 3. Docker for FastAPI

Create `Dockerfile` inside the backend folder:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## What each line does

- `FROM`: starts with Python already installed.
- `WORKDIR`: creates and enters the app folder.
- `COPY`: copies files into the image.
- `RUN`: runs a command while building the image.
- `USER`: runs the app as a normal user, not root.
- `EXPOSE`: tells us the app uses port `8000`.
- `CMD`: starts FastAPI when the container starts.

## `.dockerignore`

```text
.git
.env
.venv
__pycache__
*.pyc
```

This stops unwanted files and passwords from entering the image.

## Important

- Use `0.0.0.0` inside Docker.
- Do not use `--reload` in production.
- Keep passwords outside the image.
- Add `/health` and `/ready` routes.

