# 1. Big Picture Architecture

## Complete flow

```text
                         COLLECTION SIDE

 Scheduler
    │ every 15 min / 1 hour / daily
    ▼
 Source connector tasks
    │
    ├── Company careers connector
    ├── Allowed job-board API/feed connector
    └── Approved public-listing connector
    │
    ▼
 Redis queue
    │
    ▼
 Ingestion worker
    │
    ├── Parse source response
    ├── Convert to one common job shape
    ├── Validate required fields
    ├── Remove / merge duplicates
    └── Save results
    │
    ▼
 PostgreSQL
    │
    ├── Clean jobs                 ← portal reads from here
    ├── Source postings             ← one record per source listing
    ├── Companies / locations
    └── Scrape runs / errors

                         USER SIDE

 React frontend → FastAPI API → PostgreSQL
```

## Why there are two sides

```text
Wrong: user search → scrape five portals → slow, unreliable, possibly blocked

Right: scheduled collectors → saved clean jobs → user search is fast
```

The collector side can be slow and fail. The user side should only read already-saved data.

## Important words

| Term | Meaning |
|---|---|
| Source | One place where jobs come from |
| Connector | Small source-specific module that fetches one source |
| Raw job | Data exactly as received from a source |
| Normalized job | Your common shape: title, company, location, URL, etc. |
| Queue | A waiting line of background tasks |
| Worker | A process that completes tasks from the queue |
| Canonical job | One clean job in your portal, even if many sources list it |

## Start as one deployable application

```text
One repository / one FastAPI codebase
├── API process       → serves React requests
├── Worker process    → runs collection and processing tasks
└── Scheduler process → adds collection tasks on a timetable
```

Same codebase and database, but separate processes. This is simpler than microservices and is production-worthy for an early product.
