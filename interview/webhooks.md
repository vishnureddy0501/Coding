# Webhooks — High-Level Interview Notes

## Simple definition

> A webhook is a way for one application to notify another application automatically when an event happens.

Instead of repeatedly asking a provider whether anything changed, our application exposes an HTTP endpoint. The provider sends an HTTP request to that endpoint when an event occurs.

## Simple example

Without a webhook:

```text
Aviso asks Zoom every minute: "Was a meeting updated?"
```

With a webhook:

```text
Meeting is updated in Zoom
        ↓
Zoom sends an HTTP POST request to Aviso
        ↓
Aviso updates the meeting in its database
```

This is similar to a notification. Zoom informs Aviso instead of Aviso continuously checking Zoom.

---

## Webhook flow

```text
An event happens in provider system
        ↓
Provider sends POST request to our webhook URL
        ↓
Our server verifies the request
        ↓
Our server stores the event
        ↓
Return 200/204 quickly
        ↓
Background worker processes the event
        ↓
Application database is updated
```

Example webhook URL:

```http
POST https://api.example.com/webhooks/zoom
```

Example Zoom event:

```json
{
  "event": "meeting.updated",
  "event_ts": 1789981200000,
  "payload": {
    "account_id": "zoom_account_101",
    "object": {
      "id": 9876543210,
      "host_id": "zoom_user_55",
      "topic": "Quarterly Business Review",
      "start_time": "2026-09-25T10:00:00Z"
    }
  }
}
```

---

## High-level design

```text
Zoom / Stripe / GitHub
        ↓ webhook event
Load balancer or API gateway
        ↓
Webhook endpoint in Express.js
        ├── Verify signature
        ├── Check duplicate event
        ├── Store event
        └── Add job to queue
                    ↓
             Background worker
                    ↓
              Application DB
```

The endpoint should do minimum work and respond quickly. Slow business logic should run in a background worker.

---

## Express.js example

```js
app.post('/webhooks/zoom', async (req, res) => {
  // 1. Confirm the request really came from Zoom.
  if (!isValidZoomSignature(req)) {
    return res.status(401).send('Invalid signature');
  }

  const event = req.body;
  const eventId = createEventId(event);

  // 2. Ignore an event that was already accepted.
  const alreadyExists = await WebhookEvent.exists({ eventId });
  if (alreadyExists) {
    return res.sendStatus(200);
  }

  // 3. Save first so the event is not lost.
  await WebhookEvent.create({
    eventId,
    provider: 'zoom',
    eventType: event.event,
    payload: event,
    status: 'pending'
  });

  // 4. Process asynchronously.
  await webhookQueue.add('process-zoom-event', { eventId });

  // 5. Acknowledge quickly.
  return res.sendStatus(200);
});
```

In production, signature verification may need the original raw request body. Follow the provider's verification requirements before parsing or modifying it.

---

## How webhook security works

Never trust a webhook only because it reached the correct URL.

Common verification flow:

```text
Provider signs request using a shared secret
        ↓
Request contains signature and timestamp headers
        ↓
Our server calculates the expected signature
        ↓
Compare signatures using a timing-safe comparison
        ↓
Reject the request if they do not match
```

Important checks:

- Use HTTPS.
- Verify the provider's signature.
- Validate the timestamp to prevent replay attacks.
- Keep the webhook secret in a secret manager.
- Validate the request structure.
- Do not trust `tenantId` or `accountId` sent by an unknown caller.
- Log rejected requests without exposing secrets.

For Zoom, the event contains a Zoom `account_id`. Aviso uses its integration mapping to find the internal `tenantId`:

```text
Zoom payload.account_id
        ↓
Integration lookup
        ↓
Aviso tenantId
```

---

## Why the provider sends the same event more than once

Providers usually retry when:

- Our endpoint times out.
- Our server returns an error.
- The network fails before the response reaches the provider.

Even if our server processed the first request, the provider may not have received the response. Therefore, webhook delivery is normally **at least once**, not exactly once.

Our processing must be **idempotent**: processing the same event multiple times should produce the same final result.

### Duplicate handling

Store a unique provider event ID when one is available:

```json
{
  "eventId": "provider_event_101",
  "provider": "zoom",
  "eventType": "meeting.updated",
  "status": "processed"
}
```

Create a unique database index on:

```text
provider + eventId
```

If the provider does not supply an event ID, derive a stable key from reliable fields such as provider, event type, object ID, and event timestamp. This is less reliable, so use the provider ID whenever possible.

Use an upsert for the business record:

```text
tenantId + externalMeetingId + occurrenceId
```

---

## Why return `200` quickly?

The provider expects a fast acknowledgement. If our endpoint performs many database and external API calls before responding, it may time out and the provider may send the event again.

Recommended approach:

```text
Verify → Save → Queue → Return 200 → Process in worker
```

Return a success response only after the event has been stored reliably or placed on a durable queue.

Do not return `200` before saving it somewhere reliable; the event could be lost if the process crashes.

---

## Processing failures and retries

The background job can fail because of a temporary database, network, or provider API problem.

```text
First attempt fails
        ↓
Retry after a short delay
        ↓
Increase delay after each failure
        ↓
After maximum attempts, move to dead-letter queue
        ↓
Alert and investigate
```

Example states:

```text
received → processing → processed
                    ↘ retrying
                    ↘ failed
```

Store the attempt count and last error. Use exponential backoff for temporary failures and a dead-letter queue for events that repeatedly fail.

---

## What if a webhook is missed?

Do not depend only on webhooks. Combine them with a scheduled reconciliation job.

```text
Webhooks
    → Fast updates

Scheduled API synchronization
    → Finds missed or inconsistent updates
```

Zoom example:

```text
Every few hours
        ↓
Fetch upcoming meetings from Zoom API
        ↓
Compare with meetings in Aviso DB
        ↓
Insert missing meetings
        ↓
Update changed meetings
        ↓
Mark cancelled/deleted meetings correctly
```

This is sometimes called **reconciliation** or an **anti-entropy sync**.

---

## Event ordering problem

Webhooks may arrive out of order.

Example:

```text
meeting.updated occurred at 10:05
meeting.created occurred at 10:00

But the update reaches our server first.
```

Do not assume delivery order. Store the provider's event time or version and avoid overwriting newer data with an older event. When the correct state is unclear, fetch the latest object from the provider API.

---

## Webhook versus polling

| Webhook | Polling |
|---|---|
| Provider pushes an update | Our application repeatedly asks for updates |
| Near real-time | Depends on polling interval |
| Fewer unnecessary API calls | Can create many empty API calls |
| May be duplicated or missed | Can recover data by scanning a time range |

The best reliable design often uses both:

```text
Webhook for speed + scheduled polling for recovery
```

---

## What should be stored?

Keep a webhook inbox or event collection:

```json
{
  "eventId": "event_101",
  "provider": "zoom",
  "tenantId": "tenant_501",
  "eventType": "meeting.updated",
  "objectId": "9876543210",
  "receivedAt": "2026-09-22T10:05:01Z",
  "providerEventAt": "2026-09-22T10:05:00Z",
  "status": "processed",
  "attempts": 1,
  "lastError": null
}
```

Raw payloads are useful for debugging and replay, but they may contain personal or sensitive data. Encrypt or redact them, restrict access, and apply a retention period.

Useful database indexes:

```text
unique(provider, eventId)
(status, receivedAt)
(tenantId, eventType, receivedAt)
```

---

## Monitoring

Track:

- Events received per provider
- Invalid signatures
- Duplicate events
- Processing success and failure counts
- Time between provider event and completed processing
- Queue size and oldest pending event
- Retry and dead-letter counts
- Last successful webhook and reconciliation times

Alert when events stop arriving unexpectedly, failures increase, or the queue becomes old.

---

## Interview answer

> A webhook allows a provider to notify our backend when an event occurs. We expose an HTTPS endpoint, verify the request signature and timestamp, identify the tenant from the integration mapping, store the event, place it on a durable queue, and return `200` quickly. A background worker processes the event and updates the application database.
>
> Webhook delivery is normally at least once, so duplicate events are expected. We make processing idempotent by storing a unique event ID and upserting business records using stable external identifiers. We use retries with exponential backoff and move repeatedly failing events to a dead-letter queue.
>
> Webhooks can also be missed or delivered out of order. Therefore, we store provider timestamps, avoid replacing newer data with older events, and run a scheduled reconciliation job that compares provider data with our database.

## Short answer

> A webhook is an HTTP callback sent by a provider when something changes. The safe flow is: verify, deduplicate, store, queue, acknowledge quickly, process asynchronously, and periodically reconcile with the provider API.

```text
Event → Verify → Deduplicate → Store → Queue → 200 → Process → Reconcile
```
