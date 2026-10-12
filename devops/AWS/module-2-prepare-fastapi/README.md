# Module 2 — Prepare FastAPI for AWS

## Goal

Build the application once, then run the same Docker image in development and production with different configuration.

## Lessons

1. [Environment configuration](1.environment-configuration.md)
2. [MongoDB and health checks](2.mongodb-and-health.md)
3. [Docker and Nginx](3.docker-and-nginx.md)
4. [Run and verify dev/prod](4.run-and-verify.md)

## What was added to the app

```text
fast-api-app/
├── app/
│   ├── config.py          # reads and validates environment variables
│   ├── database.py        # MongoDB lifecycle and ping
│   └── main.py            # startup, shutdown, /health, and /ready
├── deploy/nginx/
│   └── fastapi.conf       # reverse proxy configuration
├── .env.development.example
├── .env.production.example
├── .dockerignore
├── compose.yaml
└── Dockerfile
```

Module 2 only prepares and tests the application. Creating IAM roles, EC2, ECR, and the load balancer happens in later modules.
