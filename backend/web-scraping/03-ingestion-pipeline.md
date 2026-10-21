# 3. Ingestion Pipeline

## One collected job's journey

```text
1. Scheduler adds “collect Source A” task.
2. Worker fetches one page or API response.
3. Connector parses each listing.
4. Convert listing into the common job shape.
5. Validate title, company, URL, and source data.
6. Find an existing source posting or duplicate job.
7. Insert or update database records.
8. Mark stale listings inactive when they disappear.
9. Record run result, counts, duration, and errors.
```

## Normalize before saving

Keep both original text and normalized text.

```text
Original:   "Software Engineer - Backend"
Normalized: "software engineer backend"
```

Normalization examples:

- Trim spaces and normalize letter case for matching.
- Convert Remote / Work from home to `remote`.
- Standardize known company and location names.
- Remove tracking parameters from apply URLs.

## Deduplication: the most important problem

### Same source listing collected again

Use a database unique identity:

```text
(source_id, source_job_id)
```

If the source has no stable ID:

```text
(source_id, normalized_apply_url)
```

This must be a database constraint, not only Python logic.

### Same job from different sources

Calculate a conservative match score using:

```text
normalized company + normalized title + location + similar description + posting date
```

At first, it is better to show two similar jobs than to incorrectly merge two different openings.

## Upsert, not blind insert

```text
Existing source job → update title, description, last_seen_at, active state
New source job      → create source posting and canonical job
```

## Stale jobs

```text
Not seen once        → keep it
Not seen for 7 days  → mark inactive
Inactive for 90 days → archive or delete based on your retention policy
```

This prevents a temporary source failure from removing jobs immediately.
