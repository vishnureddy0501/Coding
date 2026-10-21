# 7. Local, Dev, and Production

## Local development

```text
FastAPI API + one worker + Redis + local PostgreSQL
```

Use one safe test source or saved example source responses. Do not repeatedly hit real portals while developing a parser.

```text
Saved source response → connector parser → local database
```

This keeps local work fast and avoids unnecessary requests.

## Shared dev environment

```text
Dev FastAPI API + dev worker + dev Redis + dev PostgreSQL
```

Use different database credentials and different enabled sources from production. QA and frontend use the dev API URL.

## Production

```text
Load balancer / Nginx
        │
   FastAPI API replicas
        │
   PostgreSQL + Redis
        │
   Worker replicas + scheduler
```

Keep production secrets in AWS Parameter Store or Secrets Manager. EC2/ECS uses an IAM role; never put AWS access keys inside containers.

## Database migrations

Schema changes need a safe order:

```text
1. Back up / verify database
2. Run migration
3. Deploy API and workers from the same code version
4. Check health endpoint and scrape runs
```
