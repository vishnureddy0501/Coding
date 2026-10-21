# 5. Search API and Frontend

## API responsibility

The API reads clean saved jobs only. It never calls a source connector during a user request.

Typical endpoints:

```text
GET  /api/jobs?q=python&location=hyderabad&remote=true&page=1
GET  /api/jobs/{job_id}
GET  /api/companies/{company_id}/jobs
POST /api/saved-jobs
GET  /api/saved-jobs
```

## Search flow

```text
React filter form
      ↓
FastAPI validates query values
      ↓
PostgreSQL query using indexes
      ↓
Pagination: 20–50 jobs
      ↓
Return jobs + total count + next-page information
```

Start with PostgreSQL filters and full-text search. Add Meilisearch or OpenSearch only for typo tolerance, synonyms, or much larger scale.

## Show freshness and source

```text
Source: Company careers
Listed: 2 days ago
Last checked: 30 minutes ago
Apply on original site →
```

For the first version, send users to the original application URL.

## Pagination

Start simply:

```text
page=1&limit=20
```

Move to cursor pagination later only when the data volume makes it necessary.
