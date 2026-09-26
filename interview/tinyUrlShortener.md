# TinyURL / URL Shortener — Interview Notes

## Problem

Convert a long URL into a short URL:

```text
https://example.com/products/mobile/12345
                    ↓
https://tiny.app/aZ91Kd
```

When someone opens the short URL, redirect them to the original URL.

---

## Requirements

### Functional

- Create a short URL.
- Redirect to the original URL.
- Optionally support expiration and custom aliases.
- Track click count asynchronously.

### Non-functional

- Redirects must be very fast.
- Short codes must be unique.
- The service must handle high read traffic.
- Existing links should remain available.

This is a **read-heavy system** because a URL is normally created once but opened many times.

---

## High-level design

```text
Create URL
Client → Load Balancer → URL Service → ID Generator → Database

Open URL
Client → Load Balancer → Redirect Service → Redis Cache
                                           ↓ cache miss
                                        Database
                                           ↓
                                      HTTP redirect

Redirect Service → Queue → Analytics Worker → Analytics DB
```

---

## APIs

### Create a short URL

```http
POST /api/urls
```

```json
{
  "longUrl": "https://example.com/products/123",
  "expiresAt": "2027-01-01T00:00:00Z"
}
```

Response:

```json
{
  "shortUrl": "https://tiny.app/aZ91Kd"
}
```

### Redirect

```http
GET /aZ91Kd
```

Response:

```http
HTTP 302 Found
Location: https://example.com/products/123
```

Use `302` when click tracking and future destination changes matter. Use `301` for a truly permanent redirect that browsers may cache aggressively.

---

## Database model

```json
{
  "shortCode": "aZ91Kd",
  "longUrl": "https://example.com/products/123",
  "createdAt": "2026-09-23T10:00:00Z",
  "expiresAt": "2027-01-01T00:00:00Z",
  "status": "active"
}
```

Important database rules:

- Create a unique index on `shortCode`.
- Store expiration time if links can expire.
- Do not update click count during every redirect; send an analytics event instead.

---

## Best way to generate the short code

Use a unique numeric ID and encode it using **Base62**.

Base62 characters:

```text
a-z + A-Z + 0-9 = 62 characters
```

Example:

```text
Database ID:  125000
Base62 code:  Xwi
Short URL:    https://tiny.app/Xwi
```

### Why Base62?

- Short and URL-friendly
- No special characters
- Unique input IDs produce unique codes
- No repeated random-code collision checks

### Where does the unique ID come from?

At small scale, use a database sequence or auto-increment ID.

At large scale, use a distributed ID generator such as a Snowflake-style service:

```text
Timestamp + machine ID + sequence number
                    ↓
              Unique numeric ID
                    ↓ Base62
                 Short code
```

This lets multiple URL-service instances create codes without coordinating for every request.

> Sequential IDs can reveal creation volume. If that matters, scramble the ID before Base62 encoding or use a random Base62 code with a unique index and retry on collision.

---

## Creating a short URL

```text
1. Validate the long URL
2. Generate a unique numeric ID
3. Convert the ID to Base62
4. Store shortCode → longUrl in the database
5. Optionally add it to Redis
6. Return the short URL
```

Pseudo-code:

```js
async function createShortUrl(longUrl) {
  validateUrl(longUrl);

  const id = await idGenerator.nextId();
  const shortCode = toBase62(id);

  await urls.insert({ shortCode, longUrl });
  return `https://tiny.app/${shortCode}`;
}
```

---

## Redirecting a short URL

```text
Request /aZ91Kd
        ↓
Look in Redis
        ↓
Cache hit? ── Yes → Return redirect
        ↓ No
Read database
        ↓
Check status and expiration
        ↓
Store in Redis
        ↓
Return redirect
```

Pseudo-code:

```js
async function redirect(shortCode, res) {
  let longUrl = await redis.get(shortCode);

  if (!longUrl) {
    const url = await urls.findOne({ shortCode, status: 'active' });

    if (!url || url.expiresAt < new Date()) {
      return res.sendStatus(404);
    }

    longUrl = url.longUrl;
    await redis.set(shortCode, longUrl, { EX: 3600 });
  }

  await analyticsQueue.add('url-clicked', { shortCode });
  return res.redirect(302, longUrl);
}
```

Redis is not the source of truth. If Redis fails or the value is missing, read from the database.

---

## Why use Redis?

Popular links may receive millions of redirects.

```text
Without cache: Every redirect reads the database
With cache:    Popular redirects are served from memory
```

Use the **cache-aside pattern**:

```text
Check cache → Miss → Read DB → Update cache
```

Set a TTL so stale and expired links do not remain forever.

---

## Click analytics

Do not delay a redirect while updating analytics.

```text
Redirect request
    ├── Return destination quickly
    └── Publish click event to queue
                       ↓
                Analytics worker
                       ↓
                 Analytics DB
```

Possible metrics:

- Total clicks
- Daily clicks
- Country
- Browser/device
- Referrer

Analytics can be eventually consistent because a small delay does not affect redirection.

---

## Scaling

### Application servers

Keep URL and redirect services stateless. Add more instances behind a load balancer.

### Database

- Index `shortCode`.
- Add read replicas for redirect lookups.
- At very large scale, shard by a hash of `shortCode`.

### Cache

- Cache popular URLs in Redis.
- Use Redis Cluster when one Redis server is insufficient.
- Protect the database from a cache stampede for extremely popular keys.

### Multi-region

- Serve redirects from the nearest region.
- Replicate URL mappings between regions.
- Creation can go to a primary region if strong uniqueness is required.

---

## Failure handling

| Failure | Handling |
|---|---|
| Redis unavailable | Read from database |
| Database temporarily unavailable | Retry carefully; cached URLs can still work |
| Duplicate code | Unique index rejects it; generate another code |
| Analytics queue unavailable | Do not block redirects; buffer or drop non-critical analytics |
| Expired/deleted URL | Return `404` or an expired-link page |

---

## Security

- Accept only valid `http` and `https` URLs.
- Block malicious or phishing URLs when possible.
- Apply rate limits to URL creation.
- Restrict reserved aliases such as `admin` and `api`.
- Do not expose private analytics.
- Add abuse reporting and link disabling.

---

## Important names to remember

| Requirement | Solution |
|---|---|
| Short-code generation | Unique ID + Base62 |
| Fast redirects | Redis cache |
| Permanent storage | SQL or distributed key-value database |
| Unique codes | Unique database index |
| High availability | Load balancer + stateless instances |
| Click tracking | Queue + analytics worker |
| Large database | Read replicas and sharding |
| Abuse prevention | Validation + rate limiting |

---

## Interview answer

> I would design the URL shortener as a read-heavy system. For URL creation, the service generates a unique numeric ID, converts it to Base62, stores the short-code-to-long-URL mapping in the database, and returns the short URL.
>
> For redirects, the service first checks Redis. On a cache hit, it immediately returns an HTTP redirect. On a cache miss, it reads the database, validates expiration, updates Redis, and redirects the user. Redis makes popular redirects fast, while the database remains the source of truth.
>
> Application servers are stateless and run behind a load balancer. At large scale, I would use a distributed ID generator, database read replicas, and eventually shard by the short-code hash. Click analytics are sent through a queue so they do not slow down redirects.

## Revision flow

```text
Create:   Unique ID → Base62 → Store mapping → Return short URL
Redirect: Cache → Database on miss → HTTP 302
Track:    Queue → Analytics worker
Scale:    Stateless servers → Redis → Replicas → Sharding
```

---

## Distributed ID generation — clear explanation

### Why do we need it?

Suppose many URL-service instances create short URLs at the same time:

```text
URL Server 1 ─┐
URL Server 2 ─┼─→ Need unique IDs without creating duplicates
URL Server 3 ─┘
```

A single database auto-increment value works at small scale, but every server must contact the same database to get the next number. That database can become a bottleneck.

At large scale, each server generates IDs independently using a **Snowflake-style distributed ID generator**.

### The three parts

```text
Unique ID = timestamp + machine ID + sequence number
```

| Part | Purpose |
|---|---|
| Timestamp | Identifies the current millisecond |
| Machine ID | Identifies which server generated the ID |
| Sequence number | Distinguishes multiple IDs created by the same server in the same millisecond |

### Simple example

Assume Server 5 receives three requests in the same millisecond:

```text
Timestamp       Machine ID   Sequence
1727073000000   5            0
1727073000000   5            1
1727073000000   5            2
```

Another server generates an ID at the same time:

```text
Timestamp       Machine ID   Sequence
1727073000000   8            0
```

The IDs remain unique because:

- Requests on the same server get different sequence numbers.
- Requests on different servers get different machine IDs.
- Requests at different times get different timestamps.

### How the sequence number works

Each server keeps a small counter:

```text
New millisecond starts → sequence = 0
Another request in the same millisecond → sequence = 1
Another request in the same millisecond → sequence = 2
Next millisecond starts → sequence resets to 0
```

The sequence number is not a global database sequence. It is a local counter on each ID-generator instance for the current millisecond.

If all sequence values are used within one millisecond, the generator waits for the next millisecond before creating another ID.

### Combining the parts

The generator assigns fixed bits to each part:

```text
┌─────────────────┬────────────┬──────────────┐
│ Timestamp bits  │ Machine ID │ Sequence bits│
└─────────────────┴────────────┴──────────────┘
                  ↓
        One unique numeric ID
```

Conceptually:

```js
id = timestampBits | machineIdBits | sequenceBits;
```

Bit shifting is an implementation detail. For an interview, the important idea is that the three values are packed into one number.

### Converting the ID into a short URL

The numeric ID may be long, so encode it using Base62:

```text
Unique numeric ID:  741258963147
        ↓ Base62 encoding
Short code:         dE4x91
        ↓
Short URL:          https://tiny.app/dE4x91
```

Base62 is only an encoding step. It does not create uniqueness. The distributed ID generator creates the unique number; Base62 makes that number shorter and URL-friendly.

### Complete generation flow

```text
User submits long URL
        ↓
URL service requests an ID
        ↓
Generator combines timestamp + machine ID + sequence
        ↓
Unique numeric ID is produced
        ↓
Convert numeric ID to Base62
        ↓
Store shortCode → longUrl
        ↓
Return short URL
```

### Small-scale versus large-scale choice

```text
Small system:
Database auto-increment ID → Base62

Large distributed system:
Timestamp + machine ID + local sequence → Base62
```

### Interview answer

> In a large system, multiple servers must generate unique short codes without depending on one database counter. I would use a Snowflake-style distributed ID generator. It combines the current timestamp, a unique machine ID, and a sequence number into one numeric ID. The sequence starts at zero and increments when the same server receives multiple requests in the same millisecond. It resets when the next millisecond begins. Different timestamps, machine IDs, and sequence numbers ensure uniqueness. Finally, I Base62-encode the numeric ID to produce a short, URL-safe code.

## One line to remember

```text
Timestamp tells when + machine ID tells where + sequence tells which request
                         ↓
                  Unique ID → Base62 → Short URL
```

---

## How is the sequence safely incremented?

The sequence does not change automatically. The ID generator stores two values in memory:

```text
lastTimestamp
sequence
```

For every request:

```text
currentTimestamp == lastTimestamp
    → sequence++

currentTimestamp > lastTimestamp
    → sequence = 0
    → lastTimestamp = currentTimestamp
```

Example:

```text
Time 10:00:00.100 → sequence 0
Time 10:00:00.100 → sequence 1
Time 10:00:00.100 → sequence 2
Time 10:00:00.101 → sequence resets to 0
```

The first request observed in a new millisecond performs the reset.

### What if multiple threads request an ID simultaneously?

The check and increment must be **atomic**. Protect them using a lock, synchronized method, or compare-and-swap operation.

Simple Java-style implementation:

```java
class IdGenerator {
    private long lastTimestamp = -1;
    private long sequence = 0;
    private final long machineId;

    public synchronized long nextId() {
        long currentTimestamp = System.currentTimeMillis();

        if (currentTimestamp < lastTimestamp) {
            throw new RuntimeException("Clock moved backwards");
        }

        if (currentTimestamp == lastTimestamp) {
            sequence++;

            if (sequence > MAX_SEQUENCE) {
                currentTimestamp = waitForNextMillisecond(lastTimestamp);
                sequence = 0;
            }
        } else {
            // This is the first request in a new millisecond.
            sequence = 0;
        }

        lastTimestamp = currentTimestamp;

        return combine(currentTimestamp, machineId, sequence);
    }
}
```

Because `nextId()` is synchronized, only one thread can execute this section at a time:

```text
Thread A enters → gets sequence 0 → exits
Thread B enters → gets sequence 1 → exits
Thread C enters → gets sequence 2 → exits
```

Without synchronization, two threads could both read `sequence = 0` and generate duplicate IDs.

### What about different servers?

Each server gets a different machine/worker ID and maintains its own local sequence:

```text
Server A: machineId = 1, sequence = 0, 1, 2...
Server B: machineId = 2, sequence = 0, 1, 2...
```

Both servers can use sequence `0` at the same millisecond because their machine IDs differ.

```text
timestamp=100, machine=1, sequence=0
timestamp=100, machine=2, sequence=0
```

These produce different final IDs.

The important rule is:

> Two active generator instances must never use the same machine ID.

Machine IDs can be assigned through configuration, Kubernetes StatefulSet ordinals, or a coordination service such as ZooKeeper or etcd.

### Node.js note

Normal JavaScript code in one Node.js process runs on one event-loop thread, so a small synchronous `nextId()` function cannot be interleaved in the middle. However:

### Interview answer

> The generator stores the last timestamp and current sequence in memory. If another request arrives in the same millisecond, it increments the sequence. When it observes a newer millisecond, it resets the sequence to zero. The entire check-and-update operation is protected by a lock or atomic operation, so concurrent threads cannot receive the same sequence. Different servers use different machine IDs and keep separate local sequences. If the sequence range is exhausted, the generator waits for the next millisecond.
