# Job Listing Service

FastAPI API + Kafka + PostgreSQL for collecting and listing jobs.

```text
POST /api/v1/ingestion/naukri
        │
        ▼
Naukri connector → Kafka topic → worker → PostgreSQL
                                           │
                                           ▼
                                  GET /api/v1/jobs
```

## What is implemented

- FastAPI API with liveness and database-readiness endpoints.
- Kafka producer and a separate Kafka worker consumer.
- PostgreSQL job, company, source posting, and ingestion-run tables.
- Idempotent source posting writes using `UNIQUE (source_id, source_job_id)`.
- Naukri connector in deterministic sample mode for local testing.
- Optional live mode that only reads explicitly configured, permitted pages with standard `JobPosting` JSON-LD. It does not bypass website controls.
- Non-root application container, health checks, structured logs, and restart policies.

## Run locally

```bash
cd backend/web-scraping/job-listing-service
docker compose up --build -d
docker compose ps
```

Wait until `api`, `worker`, `postgres`, and `kafka` are running.

## Test the full pipeline

### 1. Check the API

```bash
curl http://localhost:8001/health/live
curl http://localhost:8001/health/ready
```

### 2. Publish sample Naukri jobs

```bash
curl -X POST "http://localhost:8001/api/v1/ingestion/naukri?query=python"
```

The API publishes two Naukri sample events to Kafka. The worker then saves them to PostgreSQL.

### 3. List saved jobs

```bash
curl "http://localhost:8001/api/v1/jobs?q=python"
```

Run the ingestion request a second time. You should still see two postings, not four. That proves the Kafka consumer is idempotent.

## Logs

```bash
docker compose logs -f api
docker compose logs -f worker
```

## Important local ports

| Service | Port |
|---|---:|
| FastAPI | `8001` |
| PostgreSQL | `5433` |
| Kafka | only inside Docker network |

PostgreSQL is intentionally on `5433`, so it does not conflict with another local PostgreSQL service using `5432`.

## Configuration

`.env` is for local development only. It is ignored by Git. Use `.env.example` as the safe template.

For production:

- Use managed PostgreSQL or a protected PostgreSQL instance.
- Use a managed Kafka offering or a properly secured Kafka cluster.
- Put secrets in AWS Parameter Store or Secrets Manager.
- Give the workload an IAM role instead of AWS access keys.
- Replace automatic local table creation with Alembic migrations.
- Run API, worker, and scheduler as separate deployments.

## Naukri live mode

The current connector defaults to `NAUKRI_MODE=sample` so you can test the entire pipeline safely. Before switching to live mode, verify the source terms and permitted access method. Set:

```env
NAUKRI_MODE=live
NAUKRI_SEARCH_URL_TEMPLATE=https://YOUR_PERMITTED_URL?query={query}
```

The connector only parses standard `JobPosting` JSON-LD. If the allowed source does not provide it, define an approved source contract before adding a source-specific parser.

## Stop and remove local data

```bash
docker compose down
```

To also remove the local PostgreSQL volume:

```bash
docker compose down -v
```
