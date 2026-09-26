# Email Scheduling and Tracking — Quick Interview Notes

## High-level design

```text
Vue UI → Express API → MongoDB → BullMQ/Redis → Email worker → Gmail API
                                                               ↓
Gmail watch → Google Pub/Sub → Sync worker → MongoDB → Activity UI
```

---

## 1. Scheduling an email

Express does not schedule jobs by itself. Use **BullMQ + Redis** in production.

```text
User selects date and time
        ↓
Express stores email with status = scheduled
        ↓
Add a delayed BullMQ job
        ↓
Worker runs at scheduled time
        ↓
Check latest status and access token
        ↓
Call Gmail users.messages.send
        ↓
Store Gmail messageId, threadId and status = sent
```

For a small project, `node-cron` can query due emails every minute. BullMQ is safer for retries, multiple servers, and persisted jobs.

### Important states

```text
scheduled → processing → sent
                       ↘ failed
```

Atomically change `scheduled` to `processing`. This prevents two workers from sending the same email.

### Important method

```http
POST /gmail/v1/users/me/messages/send
```

Gmail method: **`users.messages.send`**

Store:

```json
{
  "tenantId": "tenant_1",
  "scheduledAt": "2026-09-25T10:00:00Z",
  "status": "sent",
  "gmailMessageId": "message_101",
  "gmailThreadId": "thread_501"
}
```

---

## 2. What do we track?

- Scheduled emails
- Successfully sent emails
- Failed emails
- Replies
- Last sent and replied times

Use the Gmail `threadId` to connect a reply to the original conversation.

Open and click tracking are not directly provided by Gmail:

- **Open:** tracking pixel
- **Click:** tracked redirect URL

---

## 3. Initial or bulk sync

Run this when Gmail is connected for the first time.

```text
Call users.messages.list
        ↓
Receive message IDs and thread IDs
        ↓
Call users.messages.get for required messages
        ↓
Store required metadata in our DB
        ↓
Save the latest historyId as checkpoint
```

Important methods:

```http
GET /gmail/v1/users/me/messages
GET /gmail/v1/users/me/messages/{messageId}
```

- **`users.messages.list`** returns message IDs and thread IDs.
- **`users.messages.get`** returns the required message details.
- Use pagination through `nextPageToken`.
- Fetch only the required date range, labels, and fields.
- Upsert using `tenantId + gmailMessageId` to avoid duplicates.

We normally store metadata such as sender, recipients, subject, timestamps, message ID, thread ID, direction, and status—not every mailbox field.

---

## 4. Incremental sync

Do not download the entire mailbox every time. Store the Gmail **`historyId`** as a checkpoint.

```text
Read stored historyId
        ↓
Call users.history.list(startHistoryId)
        ↓
Receive IDs of changed messages
        ↓
Call users.messages.get for those messages
        ↓
Upsert changes in our DB
        ↓
Save the newest historyId only after success
```

Important method:

```http
GET /gmail/v1/users/me/history?startHistoryId={checkpoint}
```

Gmail method: **`users.history.list`**

The checkpoint belongs to a Gmail connection/mailbox, not to each email record. Keep it in an integration or sync-state collection.

```json
{
  "tenantId": "tenant_1",
  "userId": "user_10",
  "provider": "gmail",
  "lastHistoryId": "987654321",
  "lastSuccessfulSyncAt": "2026-09-22T10:00:00Z"
}
```

---

## 5. Near-real-time notifications

Gmail does not send the full email to our webhook. Use Gmail Watch with Google Cloud Pub/Sub.

```text
Call users.watch
        ↓
Gmail publishes mailbox-change notification to Pub/Sub
        ↓
Our endpoint receives email address + new historyId
        ↓
Run incremental sync using users.history.list
        ↓
Fetch message details and update our DB
```

Important method:

```http
POST /gmail/v1/users/me/watch
```

Gmail method: **`users.watch`**

The watch response contains `historyId` and `expiration`. Renew the watch before it expires; Google requires renewal at least every seven days and recommends daily renewal.

---

## 6. How do we recover missed events?

Use both push notifications and a scheduled reconciliation job.

```text
Pub/Sub notification → fast updates
Scheduled incremental sync → catches missed notifications
```

For example, run incremental sync every few hours using the last saved `historyId`.

If Gmail returns `HTTP 404` for `users.history.list`, the checkpoint is too old or invalid. Run a fresh bulk sync and save a new `historyId`.

Important rule:

> Update the checkpoint only after all pages and message updates are stored successfully. If processing fails, keep the old checkpoint and retry safely.

---

## 7. Mapping an email to an account

```text
Sender/recipient email
        ↓
Match CRM contact by email
        ↓
Contact gives CRM accountId
        ↓
Store accountId on email activity
```

Use exact contact email first. Company-domain matching should only be a fallback.

---

## Important names to remember

| Purpose | Name |
|---|---|
| Schedule jobs | BullMQ + Redis |
| Simple periodic job | `node-cron` |
| Send email | `users.messages.send` |
| List email IDs | `users.messages.list` |
| Read one email | `users.messages.get` |
| Incremental changes | `users.history.list` |
| Start notifications | `users.watch` |
| Notification transport | Google Cloud Pub/Sub |
| Sync checkpoint | `historyId` |
| Conversation mapping | `threadId` |

---

## Interview answer

> For scheduling, Express stores the email in MongoDB and creates a delayed BullMQ job in Redis. At the scheduled time, a worker atomically marks it as processing and calls Gmail's `users.messages.send`. We store the returned message ID and thread ID.
>
> During the first Gmail connection, we perform a bulk sync using `users.messages.list` and `users.messages.get`, then save the latest `historyId`. After that, we use `users.history.list` for incremental sync instead of downloading the whole mailbox.
>
> For near-real-time tracking, `users.watch` sends mailbox-change notifications through Google Cloud Pub/Sub. The notification triggers incremental sync. We also run a scheduled sync to recover missed notifications. If the saved history ID is no longer valid and Gmail returns `404`, we perform another bulk sync.

## Remember

```text
Schedule: Store → Queue → Worker → Send → Save IDs
Sync:     Bulk once → Save historyId → Incremental sync
Track:    Watch → Pub/Sub → history.list → Update DB
Recover:  Scheduled sync; 404 → Full sync
```
