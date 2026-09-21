# Support Ticket Synchronization — Incremental Sync and Recovery

## Overview

Normally, the system performs a **full synchronization only once**. After the initial import, it runs an **incremental synchronization**—for example, every 12 hours.

The overall strategy is:

```text
Initial bulk import
        ↓
Save synchronization checkpoint
        ↓
Incremental synchronization every 12 hours
        ↓
Fetch only created or modified tickets
        ↓
Idempotently upsert tickets
        ↓
Advance checkpoint only after success
        ↓
Periodically reconcile a larger historical window
```

---

# 1. Initial Bulk Synchronization

During the first synchronization, retrieve all historical tickets using pagination:

```text
Page 1 → tickets 1–100
Page 2 → tickets 101–200
Page 3 → tickets 201–300
...
```

For every ticket, store fields such as:

- External ticket ID
- Source system
- Tenant ID
- Account ID
- Status and priority
- Source creation time
- Source update time
- Local synchronization time

After successfully processing each page, save its cursor or checkpoint. This makes the import resumable if the process stops midway.

---

# 2. Incremental Synchronization

Most ticketing systems expose one or more change-tracking fields:

```text
createdAt
updatedAt
modifiedAt
version
cursor
```

Every 12 hours, request tickets whose `updatedAt` value is later than the previous successful checkpoint:

```http
GET /tickets?updated_after=2026-09-20T00:00:00Z
```

This normally returns:

- Tickets created after the checkpoint
- Existing tickets modified after the checkpoint
- Tickets that were closed or reopened
- Tickets that were reassigned
- Tickets whose status, priority, or other fields changed

Separate created-ticket and updated-ticket queries are generally unnecessary when `updatedAt` changes for both creation and modification.

---

# 3. Do Not Use Only the Current Execution Time

Suppose the previous job started at 12:00 and the next job starts at 00:00:

```text
Previous successful sync time = 12:00
Current job time              = 00:00
Query window                  = 12:00–00:00
```

A ticket might be updated at 23:59 but become visible through the provider API at 00:02 because of indexing or replication delay. The current execution may not receive it, while the next execution starts after 00:00. That ticket could be missed permanently.

Prefer the source system's incremental cursor or the maximum successfully processed source `updatedAt` value over the local job-start time.

---

# 4. Use an Overlap Window

Each synchronization should intentionally reread part of the previous time window:

```text
Previous checkpoint = 2026-09-20 12:00
Overlap             = 30 minutes
Next query starts   = 2026-09-20 11:30
```

Conceptually:

```js
const syncFrom = previousCheckpoint - overlapDuration;
```

The overlap protects against:

- Delayed provider indexing
- Clock differences between systems
- Updates occurring at the exact boundary
- Temporary API inconsistencies
- Pages processed immediately before a crash

Depending on the provider's consistency guarantees, the overlap might be five minutes, thirty minutes, or several hours.

Rereading records is safe when synchronization uses idempotent upserts.

---

# 5. Use Idempotent Upserts

Give every external ticket a unique composite identity:

```text
tenantId + sourceSystem + externalTicketId
```

Processing then follows this rule:

```text
Ticket exists         → update it
Ticket does not exist → insert it
```

## MongoDB example

```js
await tickets.updateOne(
  {
    tenantId,
    sourceSystem: "zendesk",
    externalTicketId: sourceTicket.id
  },
  {
    $set: {
      accountId,
      status: sourceTicket.status,
      priority: sourceTicket.priority,
      subject: sourceTicket.subject,
      sourceUpdatedAt: sourceTicket.updatedAt,
      syncedAt: new Date()
    }
  },
  {
    upsert: true
  }
);
```

Create a unique database index:

```js
db.tickets.createIndex(
  {
    tenantId: 1,
    sourceSystem: 1,
    externalTicketId: 1
  },
  {
    unique: true
  }
);
```

This makes overlapping synchronization safe because repeated tickets are updated instead of duplicated.

---

# 6. Advance the Checkpoint Only After Success

The checkpoint must represent completed work:

```text
Fetch page
    ↓
Validate and transform records
    ↓
Upsert all records
    ↓
Save page cursor or checkpoint
    ↓
Fetch next page
```

Do not advance the final checkpoint when:

- The API request fails
- A page cannot be retrieved
- Database writes fail
- The synchronization process crashes
- Records required for completing the page remain unprocessed

If synchronization fails, the next execution starts from the last successful checkpoint and processes the incomplete window again.

---

# 7. Handling an Individual Failed Ticket

One invalid ticket should not always cause thousands of successfully processed tickets to fail.

Use two levels of recovery:

```text
Synchronization checkpoint
    → Tracks successfully retrieved pages or windows

Failed-record queue
    → Tracks individual tickets that could not be processed
```

Example failed-record entry:

```json
{
  "tenantId": "tenant_1007",
  "sourceSystem": "zendesk",
  "externalTicketId": "987654",
  "attemptCount": 2,
  "error": "Unknown account mapping",
  "nextRetryAt": "2026-09-21T14:00:00Z",
  "payloadReference": "object-storage-reference"
}
```

The failed ticket can then be retried independently.

However, if failures indicate a system-wide problem—for example, the database is unavailable—the complete page or synchronization job should fail without advancing the checkpoint.

---

# 8. Recovering Missed Tickets Automatically

Use several protections together.

## A. Retry temporary failures

```text
Attempt 1 fails → wait 1 minute
Attempt 2 fails → wait 5 minutes
Attempt 3 fails → wait 30 minutes
Final failure   → dead-letter queue
```

Use exponential backoff with jitter so many failed records do not retry simultaneously.

## B. Resume from the last successful checkpoint

If the job crashes halfway through, the checkpoint remains behind the failed work. The next execution retrieves that data again.

## C. Use an overlap window

The next execution intentionally rereads records near the previous boundary.

## D. Run periodic reconciliation

Incremental synchronization alone may not detect every inconsistency.

For example:

```text
Every 12 hours → incremental synchronization
Every week     → reconciliation synchronization
Every month    → optional complete audit
```

A reconciliation job can:

- Refetch recently modified tickets over a larger period
- Compare source and local ticket counts
- Compare ticket IDs and update timestamps
- Find source tickets missing locally
- Find stale local tickets
- Refetch mismatched records

Example:

```text
Weekly reconciliation
        ↓
Refetch tickets updated during the previous 7–14 days
        ↓
Idempotently upsert every returned ticket
```

Because processing is idempotent, reprocessing existing tickets is safe.

---

# 9. Prefer Provider Cursors When Available

Some APIs return an opaque continuation cursor:

```json
{
  "tickets": [],
  "nextCursor": "eyJwYWdlIjoyM30="
}
```

Store the cursor only after successfully processing the associated page:

```json
{
  "integrationId": "zendesk_1007",
  "lastCursor": "eyJwYWdlIjoyM30=",
  "lastSuccessfulSyncAt": "2026-09-21T12:00:00Z"
}
```

A provider-issued incremental cursor is generally safer than a manually constructed timestamp window because it follows the provider's ordering and pagination rules.

---

# 10. Handle Updates During Pagination

Tickets can continue changing while a multi-page synchronization is running. Offset pagination can cause records to move between pages, resulting in duplicates or omissions.

Prefer:

- Provider incremental-export endpoints
- Cursor-based pagination
- Stable ordering using `updatedAt` and ticket ID
- A fixed upper boundary for the current execution

For a timestamp-based synchronization:

```text
syncFrom  = previous checkpoint − overlap
syncUntil = current time − safety delay
```

Query using a half-open interval:

```text
updatedAt >= syncFrom
AND updatedAt < syncUntil
ORDER BY updatedAt, externalTicketId
```

Use both `updatedAt` and `externalTicketId` as the pagination position because several tickets can share the same timestamp.

The next iteration starts from the completed boundary, again applying the overlap.

---

# 11. Synchronization State

Store operational state for each integration:

```json
{
  "integrationId": "zendesk_1007",
  "status": "idle",
  "lastSuccessfulCursor": "provider_cursor_981",
  "lastSuccessfulSourceTimestamp": "2026-09-21T11:30:00Z",
  "lastStartedAt": "2026-09-21T12:00:00Z",
  "lastCompletedAt": "2026-09-21T12:04:00Z",
  "lastError": null
}
```

Avoid running two synchronization jobs for the same integration simultaneously. Use a distributed lock or an atomic lease with an expiration time.

The lease should expire automatically so another worker can recover if the original worker crashes.

---

# 12. Recommended Complete Strategy

```text
First execution
    ↓
Paginated historical import
    ↓
Save provider cursor or source checkpoint
    ↓
Every 12 hours
    ↓
Acquire integration lock
    ↓
Read previous successful checkpoint
    ↓
Subtract overlap window
    ↓
Set fixed upper boundary
    ↓
Fetch changed tickets using cursor or updatedAt
    ↓
Validate and idempotently upsert
    ↓
Retry individual temporary failures
    ↓
Save checkpoint only after successful processing
    ↓
Release lock
```

Add periodic repair:

```text
Weekly reconciliation
    ↓
Refetch a larger recent window
    ↓
Detect missing or stale tickets
    ↓
Upsert corrections automatically
```

---

# 13. Important Monitoring

Track metrics such as:

- Last successful synchronization time
- Current synchronization duration
- Pages and records processed
- Records inserted and updated
- Failed-record count
- Retry and dead-letter queue size
- Provider API error and rate-limit count
- Synchronization lag: `now - latest source update processed`
- Reconciliation mismatches
- Lock age and expired-lock recovery count

Create alerts when:

- A scheduled synchronization does not complete
- Synchronization lag crosses the acceptable threshold
- Failed records continue increasing
- The dead-letter queue is not being drained
- Reconciliation finds an unusual number of missing records
- The same integration remains locked beyond the lease period

---

# 14. Interview-Ready Answer

> The first execution performs a paginated historical import. Subsequent executions do not fetch the complete dataset; they use the source system's incremental cursor or query tickets whose `updatedAt` value is later than the last successful checkpoint.
>
> We include an overlap window so boundary updates and delayed provider indexing are processed again. Processing is idempotent: each ticket is upserted using a unique key composed of tenant, source system, and external ticket ID.
>
> We update the checkpoint only after successful processing. If a job fails, the next execution resumes from the previous checkpoint, so failed work is retrieved again. Individual malformed records go to a retry or dead-letter queue.
>
> Finally, we run periodic reconciliation over a larger historical window to detect and repair any ticket that was missed because of provider delays, webhook failures, or earlier processing errors.

## Short answer

> After the initial bulk import, we perform incremental synchronization using a provider cursor or the ticket's `updatedAt` value. We use an overlap window, idempotent upserts, and checkpoints that advance only after success. Temporary failures are retried, and periodic reconciliation automatically repairs missed or stale tickets.

## Core formula to remember

```text
Incremental cursor
+ overlap window
+ idempotent upsert
+ checkpoint after success
+ retries
+ periodic reconciliation
= reliable synchronization
```

---

# 15. Preparation Checklist

Before describing this as your implementation, confirm:

- Which ticketing provider was integrated?
- Did it provide a cursor, `updatedAt`, or both?
- What was the actual synchronization frequency?
- How much overlap was configured?
- Was pagination cursor-based or offset-based?
- How was the integration lock implemented?
- Which fields formed the unique ticket key?
- Where were failed records stored?
- How many retry attempts were allowed?
- Was periodic reconciliation implemented?
- What monitoring and alerts existed?

If you did not directly implement a part, say:

> I did not directly implement that component, but my understanding of the reliable synchronization design is...
