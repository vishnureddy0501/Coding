# 4. Database Design

## Recommended primary database: PostgreSQL

Use PostgreSQL as the source of truth.

- Job search needs many filters: title, location, experience, company, date, remote.
- Unique constraints stop duplicate source records safely.
- Relations make the model clean: one job can have many source postings.
- Indexes keep filtered queries fast.
- `JSONB` can store raw source data, so MongoDB is not needed at first.

MongoDB is good for flexible raw documents. PostgreSQL is better as the main database for this job platform.

## Tables and relationships

```text
sources
  └── source_postings ──┐
                         ├── canonical_jobs ── companies
                         │         │
                         │         ├── job_locations
                         │         └── job_skills
scrape_runs ─────────────┘
users ─── saved_jobs ─── canonical_jobs
```

## `sources`

One row per portal or company feed.

```text
id
name
base_url
enabled
fetch_frequency_minutes
rate_limit_per_minute
last_success_at
```

## `canonical_jobs`

This is the main table shown to users.

```text
id
company_id
title
normalized_title
description
normalized_description
workplace_type
employment_type
experience_min
experience_max
posted_at
first_seen_at
last_seen_at
is_active
dedupe_key
created_at
updated_at
```

`dedupe_key` can be a fingerprint like:

```text
normalized_company | normalized_title | normalized_location
```

It helps find likely cross-source duplicates. Do not trust it as the only rule until you validate its results.

## `source_postings`

One row per actual listing received from a source.

```text
id
canonical_job_id
source_id
source_job_id
source_url
apply_url
raw_payload_json
first_seen_at
last_seen_at
is_active
```

Important constraint:

```text
UNIQUE (source_id, source_job_id)
```

Use a normalized URL or hash when no source job ID exists.

## Other useful tables

```text
companies:    id, name, normalized_name, website, logo_url
locations:    id, city, state, country, normalized_name
job_locations: job_id, location_id
saved_jobs:   user_id, canonical_job_id, created_at
scrape_runs:  source_id, status, started_at, finished_at,
              jobs_found, jobs_created, jobs_updated, error_message
```

For a simple first version, keep `location_text` directly on `canonical_jobs`; add location tables when multi-location jobs become important.

## Important indexes

```text
canonical_jobs(is_active, posted_at DESC)
canonical_jobs(company_id)
canonical_jobs(workplace_type)
canonical_jobs(employment_type)
source_postings(source_id, source_job_id) UNIQUE
source_postings(canonical_job_id)
```

Later, add full-text search indexes for title and description. Do not add every possible index on day one: indexes improve reads but slow writes.

## Redis is not your database

Use Redis for the queue, temporary cache, rate-limit counters, and short-lived locks. PostgreSQL remains durable source of truth.
