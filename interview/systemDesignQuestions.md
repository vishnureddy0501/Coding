# Important High-Level System Design Questions

## How to answer any system-design question

Use this order:

```text
1. Clarify requirements
2. Estimate scale
3. Define APIs and data model
4. Draw the high-level design
5. Explain the main request flow
6. Discuss scaling, failures, and trade-offs
```

Always clarify:

- Read-heavy or write-heavy?
- Expected users and requests per second?
- Is strong consistency required?
- Can processing be asynchronous?
- What happens when a component fails?

---

# 1. URL Shortener

Examples: Bitly, TinyURL

## Requirements

- Convert a long URL into a short URL.
- Redirect short URLs quickly.
- Optional expiration and click count.

## Design

```text
Create short URL
Client → Load Balancer → URL Service → Database
                              ↓
                       Generate short code

Redirect
Client → Load Balancer → URL Service → Cache → Database
                              ↓
                       HTTP 301/302 redirect
```

## Data

```text
shortCode → longUrl, createdAt, expiresAt
```

## Important points

- Generate the code using Base62 or a unique ID.
- Cache popular URLs in Redis.
- Add a database index on `shortCode`.
- Send click analytics asynchronously through a queue.
- Use `301` for permanent redirects or `302` when tracking every request matters.

---

# 2. Rate Limiter

Used to restrict how many requests a user can make.

## Design

```text
Client
   ↓
API Gateway / Rate Limiter
   ↓ check counter
Redis
   ↓
Allowed → Backend API
Rejected → HTTP 429
```

## Common algorithm: Token Bucket

```text
Bucket contains tokens
        ↓
Each request consumes one token
        ↓
Tokens refill over time
        ↓
No token → Reject request
```

## Important points

- Store counters in Redis for fast atomic updates.
- Limit by user ID, tenant ID, IP, or API key.
- Return `429 Too Many Requests`.
- Token Bucket supports short traffic bursts.
- Decide whether failure should allow or block requests.

---

# 3. Notification System

Supports email, SMS, push, or in-app notifications.

## Design

```text
Application Service
        ↓
Notification API
        ↓
Message Queue
   ┌────┼─────────┐
   ↓    ↓         ↓
Email  SMS    Push Workers
   ↓    ↓         ↓
External providers
```

## Flow

1. Validate the request and user preferences.
2. Store the notification.
3. Publish a job to the queue.
4. A channel-specific worker sends it.
5. Update status to `sent` or `failed`.

## Important points

- Use queues for asynchronous processing.
- Use retries with exponential backoff.
- Use an idempotency key to prevent duplicates.
- Respect opt-outs, quiet hours, and preferences.
- Move repeatedly failing jobs to a dead-letter queue.

---

# 4. Email Scheduling System

## Design

```text
Client → Express API → Database
                         ↓
                  Delayed job queue
                         ↓
                    Email worker
                         ↓
                 Gmail/Email provider
```

## Flow

```text
Store status = scheduled
        ↓
Create delayed job
        ↓
Worker atomically claims email
        ↓
Send through provider
        ↓
Store sent/failed status
```

## Important points

- Use BullMQ with Redis or another durable job queue.
- Do not depend on an in-process timer for production.
- Use `scheduled → processing → sent/failed` states.
- Use an idempotency key to avoid duplicate sends.
- Retry temporary errors; do not endlessly retry permanent errors.

---

# 5. Chat System

Examples: WhatsApp, Slack

## Design

```text
Sender → WebSocket Gateway → Chat Service → Message DB
                 ↓                ↓
           Connection map      Message Queue
                 ↓                ↓
              Receiver ← Delivery Worker
```

## Flow

1. Sender sends a message through WebSocket.
2. Chat service stores the message.
3. Message is published to the receiver's server.
4. Receiver gets the message if online.
5. Otherwise, send a push notification.

## Important points

- Use WebSockets for real-time communication.
- Store messages before acknowledging them.
- Partition messages by `conversationId`.
- Maintain message states: `sent`, `delivered`, `read`.
- Preserve ordering inside one conversation.

---

# 6. File Upload and Storage System

Examples: Google Drive, Dropbox

## Design

```text
Client → Backend → Generate pre-signed URL
   ↓
Upload directly to Object Storage
   ↓ event
Queue → Virus scan / Thumbnail worker
   ↓
Metadata Database
   ↓
CDN for downloads
```

## Important points

- Store files in object storage, not the application database.
- Upload directly using a pre-signed URL.
- Store file metadata and permissions in a database.
- Use multipart upload for large files.
- Use a CDN for fast downloads.
- Process scans and thumbnails asynchronously.

---

# 7. News Feed

Examples: LinkedIn, Facebook

## Design

```text
Create post
User → Post Service → Post DB → Queue → Feed workers
                                         ↓
                                     Feed Cache

Read feed
User → Feed Service → Feed Cache → Post/User services
```

## Two approaches

### Fan-out on write

When a post is created, add it to every follower's feed.

- Fast reads
- Expensive for users with millions of followers

### Fan-out on read

Build the feed when the user opens it.

- Cheaper writes
- Slower reads

Large systems often use a hybrid approach.

## Important points

- Cache feed IDs in Redis.
- Use cursor pagination.
- Generate normal users' feeds on write.
- Generate celebrity content on read.
- Ranking can be a separate service.

---

# 8. Search Autocomplete

Examples: Google search suggestions, product search

## Design

```text
User types prefix
        ↓
Autocomplete API
        ↓
Redis Cache → Trie/Search Index
        ↓
Ranked suggestions

Search logs → Queue → Aggregation job → Update index
```

## Important points

- Use a Trie or search engine index for prefix lookup.
- Cache popular prefixes.
- Rank using popularity, relevance, language, and recent trends.
- Update the index asynchronously.
- Debounce requests on the frontend.
- Do not query on every keystroke unnecessarily.

---

# 9. Product Usage Analytics

Tracks actions such as login, report creation, and feature usage.

## Design

```text
Frontend / Backend events
        ↓
Event Collector
        ↓
Message Queue / Event Stream
        ↓
Processing workers
   ┌──────────────┴─────────────┐
   ↓                            ↓
Raw event storage        Aggregated metrics DB
                                  ↓
                              Dashboard
```

## Important points

- Every event contains `tenantId`, `userId`, `eventName`, and timestamp.
- Use a queue so product requests are not slowed down.
- Keep raw events for reprocessing.
- Precalculate daily or monthly aggregates.
- Deduplicate using `eventId`.
- Partition by date and tenant for large volumes.

---

# 10. Webhook Processing System

Receives events from Zoom, Stripe, Gmail, GitHub, etc.

## Design

```text
External provider
        ↓ POST event
Webhook endpoint
        ↓
Verify signature → Deduplicate → Store event → Return 200
                                        ↓
                                      Queue
                                        ↓
                                     Worker
                                        ↓
                                  Application DB
```

## Important points

- Verify signature and timestamp.
- Store the event before returning success.
- Respond quickly and process asynchronously.
- Assume events can be duplicated or out of order.
- Use the provider event ID for idempotency.
- Run scheduled reconciliation to recover missed events.

---

# 11. Ticket or External Data Synchronization

Examples: Synchronizing Zendesk tickets or CRM records.

## Design

```text
Initial bulk sync
Provider API → Paginated fetch → Queue → Workers → Local DB

Incremental sync
Checkpoint → Fetch changed records → Upsert → Save new checkpoint

Recovery
Webhooks + Scheduled reconciliation
```

## Important points

- Perform a paginated bulk sync initially.
- Store a checkpoint such as `updatedAt`, cursor, or provider token.
- Use overlapping time windows when timestamps are used.
- Upsert using `tenantId + externalId`.
- Update the checkpoint only after successful processing.
- Use periodic reconciliation to find missed records.

---

# 12. Payment System

## Design

```text
Client → Order Service → Order DB
              ↓
        Payment Provider
              ↓ webhook
        Payment Service
              ↓
       Update payment/order
              ↓
       Queue → Email/Fulfilment
```

## Important points

- Never trust only the frontend success screen.
- Confirm payment through provider API or signed webhook.
- Use an idempotency key when creating a payment.
- Maintain states such as `pending`, `paid`, `failed`, `refunded`.
- Store an immutable payment transaction history.
- Never store raw card details; use the provider's secure flow.

---

# Common building blocks to remember

| Requirement | Common solution |
|---|---|
| Fast repeated reads | Redis cache |
| Background processing | Message queue and workers |
| Large files | Object storage |
| Fast downloads | CDN |
| Real-time updates | WebSocket |
| External event notification | Webhook |
| Duplicate prevention | Idempotency key + unique index |
| Missed-event recovery | Scheduled reconciliation |
| Full-text search | Elasticsearch/OpenSearch |
| High database reads | Read replicas |
| Growing database | Partitioning/sharding |
| Service protection | Rate limiter |

---

# Common reliability concepts

## Idempotency

Repeating the same request should not create duplicate results.

```text
Same idempotency key → Return the original result
```

## Retry with exponential backoff

```text
Retry after 1s → 2s → 4s → 8s
```

Retry only temporary failures.

## Dead-letter queue

Jobs that fail repeatedly are moved aside for investigation instead of blocking the main queue.

## Cache-aside

```text
Read cache
   ↓ miss
Read database
   ↓
Update cache
```

## Database index

Indexes make reads faster but increase storage and write cost. Add them for actual query patterns.

---

# Short interview structure

> First, I clarify the functional requirements, expected scale, and consistency needs. Then I define the main APIs and data model. I draw the request flow through the load balancer, services, database, cache, and queue. Finally, I explain scaling, duplicate prevention, retries, monitoring, and failure recovery, including the trade-offs behind each choice.

## Final revision map

```text
Read performance       → Cache + index + replicas
Write scalability      → Queue + partitioning
Slow background work   → Workers
Real-time communication→ WebSocket
External updates       → Webhooks
Duplicate requests     → Idempotency
Failed jobs            → Retry + dead-letter queue
Missed external events → Reconciliation sync
Large files            → Object storage + CDN
```
