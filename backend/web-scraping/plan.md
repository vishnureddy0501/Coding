# Plan

## What you will understand

- How one application can list jobs from many sources.
- Why scraping must not happen during a user request.
- Which database stores what.
- How duplicate jobs are identified.
- How to run local, dev, and production environments.

## Recommended first stack

| Need | Start with | Why |
|---|---|---|
| API | FastAPI | Python and simple APIs |
| Collectors | Python HTTP client/parser; browser automation only when permitted | One connector per source |
| Primary database | PostgreSQL | Filters, relations, unique constraints |
| Background work | Redis + Celery or Dramatiq | Collection stays away from API requests |
| Search | PostgreSQL full-text search first | Enough for the first version |
| Later search | Meilisearch / OpenSearch | Typo-tolerant search at larger scale |
| Raw source payload | PostgreSQL JSONB first | Debug source changes |

Do not start with microservices, Kafka, Kubernetes, or a vector database. Begin as one FastAPI codebase with separate API, worker, and scheduler processes.
