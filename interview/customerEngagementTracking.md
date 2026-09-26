# Zoom Call Tracking — Interview Notes

## Simple explanation

> Aviso connects to a customer's Zoom account, regularly synchronizes scheduled and completed meetings, maps meeting participants to CRM contacts and accounts, and stores the normalized call data in its own database. This lets the UI quickly show upcoming calls, completed calls, participants, and call counts without calling Zoom every time.

---

## High-level design

```text
Customer's Zoom account
        ↓ OAuth authentication
Zoom REST APIs + webhooks
        ↓
Aviso Zoom integration service
        ↓
Normalize and map identifiers
        ↓
Aviso database
        ↓
Call APIs and dashboard
```

The integration has two responsibilities:

1. Get meeting information from Zoom.
2. Connect that information to the correct Aviso tenant and CRM account.

---

## Important identifiers

| Field | Comes from | Meaning |
|---|---|---|
| `tenantId` | Aviso | The customer organization using Aviso |
| `zoomAccountId` | Zoom | The customer's Zoom organization |
| `zoomUserId` / `hostId` | Zoom | The Zoom user hosting the meeting |
| `meetingId` | Zoom | The visible Zoom meeting number; recurring meetings may reuse it |
| `meetingUuid` | Zoom | Identifies one actual meeting instance |
| `accountId` | Aviso/CRM | The customer account, such as ABC Ltd |
| `participantId` | Zoom, when available | The Zoom identity of a participant |

### Do not confuse the two account IDs

```text
zoomAccountId = customer's organization inside Zoom
accountId     = customer/company record inside Aviso or CRM
```

They represent different things.

---

## How Aviso knows the `tenantId`

When an Aviso tenant connects Zoom, save an integration record:

```json
{
  "tenantId": "tenant_101",
  "provider": "zoom",
  "zoomAccountId": "zoom_account_xyz",
  "status": "active",
  "lastSuccessfulSyncAt": "2026-09-22T06:00:00Z"
}
```

Later, every API sync or webhook contains Zoom account/user information. Aviso finds the integration record and obtains the corresponding `tenantId`.

```text
Zoom account ID
      ↓ integration lookup
Aviso tenant ID
```

Every stored meeting must contain `tenantId` so that one customer's data cannot appear for another customer.

---

## How Aviso knows the call ID

For an upcoming meeting, Zoom returns a numeric `meetingId`. Store it as `externalMeetingId`.

For a completed meeting, also store the Zoom `meetingUuid`. This is important because a recurring meeting can use the same meeting ID many times, but every completed occurrence has a different UUID.

Recommended uniqueness:

```text
Upcoming meeting: tenantId + meetingId + occurrenceId/startTime
Completed call:   tenantId + meetingUuid
```

This prevents duplicate records during repeated synchronization.

---

## How participants are identified

There are two different participant lists.

### 1. Expected participants before the call

These are invitees or registrants.

- If Zoom registration is enabled, use:

```http
GET /v2/meetings/{meetingId}/registrants
```

- Some meeting details may contain `meeting_invitees`.
- If the meeting invitation is managed through Google or Outlook Calendar, synchronize the calendar event to obtain its attendees.

Zoom may not provide a complete invitee list for every ordinary meeting. Therefore, calendar integration is often needed for reliable scheduled-attendee information.

### 2. Actual participants after the call

Use Zoom's past-participant API:

```http
GET /v2/past_meetings/{meetingUuid}/participants
```

It can provide fields such as participant name, email when available, join time, leave time, and duration.

Participant email is not guaranteed. An external participant may join without signing in, so Zoom may return only a display name or a meeting-specific participant identifier.

---

## How a meeting is mapped to an Aviso account

Zoom does **not** know Aviso's CRM `accountId`. Aviso derives it.

Preferred matching order:

```text
Participant email
      ↓
CRM contact lookup
      ↓
Contact belongs to CRM account
      ↓
Save the Aviso accountId on the call
```

Example:

```text
asha@abc.com
      ↓
CRM contact: Asha Rao
      ↓
CRM account: ABC Ltd
      ↓
accountId = account_501
```

Matching rules:

1. Exact CRM contact email — best option
2. Existing participant-to-contact mapping
3. Verified company email domain — fallback only
4. Manual review if the result is ambiguous

Ignore the customer's own employee domains while finding the external account. Do not automatically map public domains such as `gmail.com` to a company.

A meeting can contain people from multiple customer accounts. In that case, store a many-to-many mapping instead of forcing only one `accountId`.

---

## Zoom authentication

Zoom supports two useful OAuth approaches.

### Option 1: Server-to-Server OAuth

Use this for a private, account-level integration managed by the customer's Zoom administrator.

The admin creates and activates a Server-to-Server OAuth app and grants the required read scopes. Aviso stores these securely:

```text
Zoom Account ID
Client ID
Client Secret
```

To get an access token:

```http
POST https://zoom.us/oauth/token
```

```text
grant_type=account_credentials
account_id=<ZOOM_ACCOUNT_ID>
Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)
```

Then call Zoom using:

```http
Authorization: Bearer <access_token>
```

Server-to-Server tokens are short-lived. Cache the token until shortly before expiry, then request a new one. There is no end-user login and no refresh token in this flow.

### Option 2: Standard OAuth authorization code flow

Use this when each customer or user installs and authorizes the integration.

```text
User clicks Connect Zoom
      ↓
Zoom consent screen
      ↓
Aviso receives authorization code
      ↓
Backend exchanges it for access and refresh tokens
      ↓
Encrypt and store the refresh token
```

When the access token expires, use the refresh token to obtain another one.

> Use minimum read-only meeting, user, participant, report, and webhook scopes required by the chosen APIs. Admin scopes are needed when syncing meetings for the entire Zoom account.

---

## Initial synchronization

The first sync creates the local view of Zoom data.

```text
Connect Zoom account
      ↓
Fetch Zoom users/hosts
      ↓
For each host, fetch upcoming scheduled meetings
      ↓
Fetch the required period of completed meetings
      ↓
Fetch registrants or actual participants where required
      ↓
Map participants to CRM accounts
      ↓
Upsert meetings into Aviso database
```

For meetings hosted by a user:

```http
GET /v2/users/{userId}/meetings?type=upcoming
```

For a user-level integration, `{userId}` can be `me`. For account-wide synchronization, retrieve the permitted users and synchronize each host.

Zoom also provides:

```http
GET /v2/users/{userId}/upcoming_meetings
```

This includes meetings the user hosts or is invited to, but Zoom documents it as covering only the next 24 hours. Do not use it as the only source for a long-range upcoming-meetings page.

---

## Incremental synchronization of upcoming calls

Use **webhooks plus scheduled reconciliation**.

### Webhooks for quick updates

Subscribe to events such as:

```text
meeting.created
meeting.updated
meeting.deleted
meeting.started
meeting.ended
```

When Aviso receives an event:

1. Validate the webhook.
2. Resolve `zoomAccountId` to `tenantId`.
3. Use the meeting ID to fetch complete data if needed.
4. Upsert or cancel the local meeting.
5. Recalculate its CRM account mapping.

### Scheduled reconciliation for missed events

Run a background job periodically, for example every 30 minutes or every few hours:

```text
Fetch upcoming meetings from Zoom
      ↓
Upsert by tenant + external meeting key
      ↓
Update changed time, topic, host, or status
      ↓
Mark locally stored meetings missing from Zoom as cancelled/removed
      ↓
Save lastSuccessfulSyncAt
```

Webhooks make the UI update quickly. The scheduled sync repairs missed webhooks, temporary network failures, and data differences.

Use pagination, retry temporary failures with backoff, and update the checkpoint only after a successful run.

---

## Should meetings be stored in Aviso's database?

**Yes.** Store a normalized local copy.

Reasons:

- Faster dashboard responses
- No Zoom API call on every page load
- Account-level filtering and aggregation
- Historical data and trends
- Protection from temporary Zoom outages
- Fewer rate-limit problems
- Ability to combine Zoom data with CRM data

Zoom remains the source of truth for provider fields. Aviso's database is the read-optimized application view.

Example meeting record:

```json
{
  "tenantId": "tenant_101",
  "provider": "zoom",
  "zoomAccountId": "zoom_account_xyz",
  "externalMeetingId": "9876543210",
  "meetingUuid": "instance_uuid_after_call",
  "hostZoomUserId": "zoom_user_55",
  "accountIds": ["account_501"],
  "topic": "Quarterly Business Review",
  "startTime": "2026-09-25T10:00:00Z",
  "endTime": "2026-09-25T11:00:00Z",
  "status": "scheduled",
  "participantCount": 4,
  "lastSyncedAt": "2026-09-22T10:00:00Z"
}
```

Store participants in a separate collection/table when one meeting can contain many people.

---

## Total and upcoming meeting counts

The dashboard should normally calculate counts from Aviso's database, not from Zoom in real time.

### Upcoming meetings

```text
tenantId = current tenant
accountId = selected account
startTime > now
status = scheduled
```

### Total completed meetings

```text
tenantId = current tenant
accountId = selected account
status = completed
startTime is inside selected date range
```

Example application APIs:

```http
GET /api/accounts/:accountId/calls?status=upcoming
GET /api/accounts/:accountId/calls?status=completed
GET /api/accounts/:accountId/call-summary?from=...&to=...
```

Example response:

```json
{
  "totalMeetings": 42,
  "completedMeetings": 39,
  "upcomingMeetings": 3,
  "lastMeetingAt": "2026-09-20T10:00:00Z",
  "nextMeetingAt": "2026-09-25T10:00:00Z"
}
```

For initial backfill, Zoom report/past-meeting APIs can supply completed meetings. After synchronization, MongoDB or the chosen application database should serve the counts efficiently using indexes such as:

```text
(tenantId, accountIds, status, startTime)
(tenantId, externalMeetingId, startTime) unique for scheduled occurrences
(tenantId, meetingUuid) unique when UUID exists
```

---

## Complete flow

```text
Zoom admin connects account through OAuth
        ↓
Aviso stores tenant ↔ Zoom account mapping
        ↓
Initial job fetches hosts and scheduled meetings
        ↓
Zoom meeting ID becomes externalMeetingId
        ↓
Invitee/participant email maps to CRM contact and accountId
        ↓
Normalized call is stored in Aviso database
        ↓
Webhooks update it quickly
        ↓
Scheduled reconciliation repairs missed updates
        ↓
Dashboard reads total and upcoming counts from Aviso DB
```

---

## Interview answer

> When a customer connects Zoom, we store a mapping between the Aviso tenant ID and the Zoom account ID. We authenticate using Zoom OAuth—typically Server-to-Server OAuth for an admin-approved account-wide integration, or the authorization-code flow for customer-installed integrations.
>
> Zoom provides the meeting ID, host ID, time, and meeting status. For completed occurrences, we also store the meeting UUID because recurring meetings may reuse the same meeting ID. Expected participants can come from Zoom registrants, meeting invitees, or the connected calendar; actual attendees come from the past-meeting participants API.
>
> Zoom does not know our CRM account ID. We match participant emails to CRM contacts, and the contact gives us the Aviso account ID. We store the normalized meeting and participants in our database for fast queries and aggregation.
>
> Webhooks handle meeting creation, updates, deletion, and completion quickly. A scheduled reconciliation job fetches upcoming meetings again and repairs missed webhook events. The UI reads total meetings and upcoming meetings from our database instead of calling Zoom on every request.

## Short answer

> Zoom gives us the Zoom account, meeting, host, and participant identifiers. Aviso uses the integration record to find `tenantId` and participant-to-CRM matching to find `accountId`. We sync with OAuth-protected Zoom APIs, use webhooks plus periodic reconciliation, and store a local normalized copy so meeting lists and counts are fast and reliable.
