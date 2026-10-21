# 8. Build Order

## Phase 1: one source, correct data

```text
One allowed source connector
PostgreSQL tables: sources, canonical_jobs, source_postings, scrape_runs
Manual collection run
Simple jobs-list API
```

Success: collect twice and see no duplicate source postings.

## Phase 2: usable portal

```text
React job list
Search by title
Filters: location, remote, date
Job detail page
Link to original apply URL
```

## Phase 3: background collection

```text
Redis queue
Worker
Scheduler
Retries and scrape-run records
```

## Phase 4: multiple sources

```text
Second and third connectors
Source configuration table
Basic cross-source duplicate detection
Source failure alerts
```

## Phase 5: production quality

```text
Separate dev and production environments
Database backups
Monitoring and alerts
Parameter Store / IAM role
Nginx or load balancer + HTTPS
```

## Do not build first

```text
AI matching
Resume scoring
Auto-apply
Microservices
Kafka
Kubernetes
Vector database
```

First make collection, clean data, duplicate handling, filters, and deployment reliable.
