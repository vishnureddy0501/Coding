# Support Ticket Synchronization

## Objective

Synchronize support tickets from a system such as Zendesk, ServiceNow, or Jira into our application.

The solution has three parts:

1. Perform a one-time bulk sync.
2. Perform incremental syncs every 12 hours.
3. Detect and recover tickets missed by an earlier sync.

---

# 1. Initial Bulk Sync

The first sync imports all historical tickets.

Fetch tickets page by page instead of requesting everything at once:

```text
Fetch page 1
    ↓
Transform and validate tickets
    ↓
Insert or update tickets in our database
    ↓
Save the page cursor
    ↓
Fetch the next page
```

For every ticket, store at least:

- Internal ticket ID
- External ticket ID
- Tenant ID
- Source system
- Account ID
- Status and priority
- Source `createdAt`
- Source `updatedAt`
- Local `syncedAt`

Use this composite key to uniquely identify a ticket:

```text
tenantId + sourceSystem + externalTicketId
```

Process tickets using an **upsert**:

```text
Ticket exists         → update it
Ticket does not exist → insert it
```

Upserts make it safe to process the same ticket again without creating duplicates.

---

# 2. Incremental Sync Every 12 Hours

After the bulk import, do not fetch all tickets again. Fetch only tickets created or modified after the last successful sync.

Most providers support one of these:

- An incremental cursor
- An `updatedAt` filter

Cursor example:

```http
GET /tickets?cursor=<last-successful-cursor>
```

Timestamp example:

```http
GET /tickets?updated_after=2026-09-21T00:00:00Z
```

Because a newly created ticket also has an `updatedAt` value, this query returns both:

- New tickets
- Existing tickets that changed

Examples of changes include closing, reopening, reassigning, or changing priority.

## Save the checkpoint only after success

```text
Read previous checkpoint
        ↓
Fetch changed tickets
        ↓
Upsert all tickets successfully
        ↓
Save new checkpoint
```

If the API call, database update, or job fails, do not advance the checkpoint. The next execution starts from the old checkpoint and retrieves the same tickets again.

---

# 3. Prevent Boundary Misses

A ticket updated at 11:59 may become visible through the provider API only after 12:00 because of indexing delay.

Use a small overlap window:

```text
Last successful checkpoint = 12:00
Overlap                    = 30 minutes
Next sync starts from      = 11:30
```

The next sync intentionally fetches some tickets again. This is safe because upserts prevent duplicates.

The combination is:

```text
Previous checkpoint − overlap window
```

Use the provider's incremental cursor when available because it is usually safer than managing timestamps manually.

---

# 4. How Do We Know a Ticket Was Missed?

An incremental job cannot always know immediately that one ticket is missing. For example, the provider may temporarily omit a record or an individual record may fail during processing.

Use a periodic **reconciliation sync** to detect differences.

For example:

```text
Every 12 hours → incremental sync
Every week     → resync tickets updated during the last 7–14 days
```

During reconciliation:

1. Fetch ticket IDs and `updatedAt` values from the source.
2. Compare them with the local database.
3. Find missing local ticket IDs.
4. Find tickets whose local `sourceUpdatedAt` is older.
5. Fetch and upsert the missing or stale tickets.

```text
Source ticket exists, local ticket missing
        → insert it

Source updatedAt is newer than local sourceUpdatedAt
        → update the local ticket
```

Ticket counts can help detect a possible problem, but counts alone are not enough. Two systems could have the same count while containing different tickets. Comparing ticket IDs and source update timestamps is more reliable.

---

# 5. What If One Ticket Fails?

If one ticket fails because of invalid data or a missing account mapping:

1. Record its external ticket ID and error.
2. Put it in a retry queue.
3. Continue processing other valid tickets when safe.
4. Retry it later.
5. Move it to a dead-letter queue after repeated failures.

If the entire database or provider is unavailable, fail the complete sync and keep the old checkpoint.

The reconciliation job provides another opportunity to recover an individually missed ticket automatically.

---

# Complete Flow

```text
First execution
    ↓
Fetch all historical tickets page by page
    ↓
Upsert using external ticket identity
    ↓
Save successful cursor or checkpoint
    ↓
Every 12 hours
    ↓
Fetch tickets changed after checkpoint − overlap
    ↓
Upsert tickets
    ↓
Save checkpoint only after success
    ↓
Weekly reconciliation
    ↓
Compare source IDs and updatedAt values with local data
    ↓
Repair missing or stale tickets
```

---

# Interview-Ready Answer

> The first execution performs a paginated bulk import of historical tickets. Each ticket is upserted using a unique key made from the tenant, source system, and external ticket ID.
>
> After that, a scheduled job runs every 12 hours. It uses the provider's incremental cursor or fetches tickets whose `updatedAt` value is later than the last successful checkpoint. We include a small overlap window to handle boundary updates and provider indexing delays.
>
> The checkpoint is advanced only after successful processing. If the job fails, the next execution starts from the previous checkpoint and safely processes the same records again.
>
> To find tickets that were silently missed, we run a periodic reconciliation over a larger recent window. We compare source ticket IDs and update timestamps with local records, then upsert anything missing or stale. Individual failures are retried separately and eventually moved to a dead-letter queue if they continue failing.

## Short answer

> Perform one paginated bulk import, then fetch only changed tickets using a cursor or `updatedAt`. Use an overlap window, idempotent upserts, and a checkpoint that advances only after success. Run periodic reconciliation to compare source IDs and timestamps and automatically repair missing or stale tickets.

## Formula to remember

```text
Bulk import once
+ incremental sync
+ overlap window
+ upsert
+ checkpoint after success
+ periodic reconciliation
= reliable ticket synchronization
```

where to store checkpoint?
--------------------------
I would keep synchronization state in a separate collection keyed by tenant, source system, and resource type. The job reads the last successful cursor or source timestamp before starting and advances it only after the related ticket records have been successfully upserted.

The important rule is:
    Never advance the checkpoint before the related tickets are saved successfully.

collection name: integration_sync_state

{
  "_id": "sync_1001",
  "tenantId": "tenant_1007",
  "sourceSystem": "zendesk",
  "resourceType": "tickets",
  "status": "idle",
  "lastSuccessfulCursor": "cursor_abc123",
  "lastSuccessfulSourceUpdatedAt": "2026-09-21T12:00:00Z",
  "lastStartedAt": "2026-09-22T00:00:00Z",
  "lastCompletedAt": "2026-09-22T00:04:30Z",
  "lastError": null
}