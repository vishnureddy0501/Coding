# FastAPI application

Deployment-ready FastAPI app using MongoDB Atlas, Docker, and environment-based configuration.

## Configuration

Create a local environment file from the correct template:

```bash
cp .env.development.example .env.development
```

Replace every `<...>` placeholder. Never commit the completed file. Production uses `.env.production.example` as its template and must use a different Atlas database.

## Run without Docker

```bash
uv sync
uv run fastapi dev app/main.py --env-file .env.development
```

## Run with Docker

Development:

```bash
APP_ENV_FILE=.env.development docker compose up --build
```

Production-style run using an image pulled from ECR:

```bash
APP_IMAGE=<account-id>.dkr.ecr.<region>.amazonaws.com/fastapi-app:<version> \
APP_ENV_FILE=.env.production \
docker compose up -d --no-build
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Process health: `http://127.0.0.1:8000/health`
- MongoDB readiness: `http://127.0.0.1:8000/ready`

The container listens on host loopback only. Nginx accepts web traffic on port `80` and proxies it to port `8000`. Use `deploy/nginx/fastapi.conf` on the EC2 host.

## Important behavior

- Startup fails if required settings or MongoDB are unavailable.
- `/health` is lightweight and is suitable for the Docker and ALB health check.
- `/ready` returns HTTP `503` when Atlas becomes unavailable.
- Logs go to standard output so Docker and CloudWatch can collect them.
