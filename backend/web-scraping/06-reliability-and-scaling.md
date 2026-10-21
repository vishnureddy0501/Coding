# 6. Scheduling, Failures, and Scaling

## Scheduling

```text
Frequently changing source → every 15–60 minutes
Company careers page      → every 6–24 hours
Slow or limited source    → less often
```

The scheduler only creates tasks. Workers do the actual collection.

```text
Scheduler → queue → workers
```

## Rate limits and retries

Set these per source:

```text
Maximum requests per minute
Maximum concurrent requests
Timeout
Retry count
Backoff delay
```

Example:

```text
Request fails → wait 1 minute → retry
Fails again   → wait 5 minutes → retry
Still fails   → mark run failed and alert
```

Do not retry immediately in a tight loop.

## Failure isolation

```text
Source A breaks → only Source A tasks fail
                 Source B and C continue
                 API still shows last valid jobs
```

## Monitor these values

```text
Last successful run
Duration
Jobs found
New jobs created
Errors
Queue size
```

Alert when a normally active source returns zero jobs repeatedly or has not succeeded for a set time.

## Scaling path

```text
Stage 1: one worker, PostgreSQL, Redis
Stage 2: multiple worker replicas when collection is slow
Stage 3: separate API and worker deployments
Stage 4: dedicated search engine when PostgreSQL search is not enough
```

API and worker capacity should scale separately. More users need more API capacity; more sources need more workers.
