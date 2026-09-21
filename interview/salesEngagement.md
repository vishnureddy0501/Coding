# Sales Engagement Platform — Interview and System Design Notes

Use this document to prepare a clear project explanation and answer technical follow-up questions.

## Contents

1. [Project overview](#1-project-overview)
2. [Core concepts and terminology](#2-core-concepts-and-terminology)
3. [High-level architecture](#3-high-level-architecture)
4. [Prospect management](#4-prospect-management)
5. [Sequence and workflow design](#5-sequence-and-workflow-design)
6. [Email composition and templates](#6-email-composition-and-templates)
7. [Email scheduling and execution](#7-email-scheduling-and-execution)
8. [Gmail integration](#8-gmail-integration)
9. [Email and reply tracking](#9-email-and-reply-tracking)
10. [Activity timeline](#10-activity-timeline)
11. [Reliability and failure handling](#11-reliability-and-failure-handling)
12. [Security and authorization](#12-security-and-authorization)
13. [Performance and scalability](#13-performance-and-scalability)
14. [Monitoring and testing](#14-monitoring-and-testing)
15. [Common interview questions](#15-common-interview-questions)
16. [Sales Engagement versus Customer Success Intelligence](#16-sales-engagement-versus-customer-success-intelligence)

> **Important:** These notes combine résumé information with standard, defensible system-design patterns. The exact internal architecture at Aviso may be different and is not public. Present only the features and decisions you personally worked on as your own contribution. Describe other sections as your understanding or as an improved design you would recommend.

---

# 1. Project Overview

## One-line description

> Sales Engagement is an outreach-automation platform that helps sales representatives manage prospects, create email sequences, schedule personalized communication, and track engagement from one place.

## Interview-ready explanation

> At Aviso AI, I worked on a Sales Engagement Platform that helps sales representatives organize and automate prospect outreach.
>
> The platform allows users to manage prospects, create multi-step email sequences, compose personalized emails, use AI-generated content, schedule communication, track activities, and monitor engagement from a unified interface. Its purpose is to reduce repetitive manual work and help sales representatives follow a consistent outreach process.
>
> I contributed to prospect management, email composition, templates, scheduling, activity tracking, campaign workflows, and responsive user interfaces.
>
> On the frontend, I used Vue.js and Vuex to build workflows and manage application state. I integrated Quill.js as a rich-text email editor and worked with Gmail APIs for email-related operations. On the backend, I worked with Express.js, MongoDB, and REST APIs for prospect data, activities, email workflows, and synchronization.
>
> An important challenge was maintaining consistent state across prospects, sequences, scheduled actions, and external email operations. We addressed this through clear workflow statuses, backend validation, failure handling, and targeted frontend updates.
>
> The result was a centralized workflow that made outreach easier to manage and reduced repetitive work for sales representatives.

## My role

> I worked on end-to-end feature development, including prospect-management interfaces, the rich-text email editor, Gmail integration, email scheduling, activity tracking, campaign workflows, REST API integration, and responsive UI development.

## Business problem

Without a sales-engagement platform, a representative may need to:

- Maintain prospects in spreadsheets or separate systems
- Copy and personalize each email manually
- Remember when to send follow-ups
- Switch between the CRM, inbox, calendar, and notes
- Manually record every activity
- Track responses without a consolidated timeline

The platform converts that fragmented process into a structured workflow.

---

# 2. Core Concepts and Terminology

| Concept | Meaning |
|---|---|
| Prospect | A person or organization the representative wants to contact |
| Sequence | An ordered set of outreach steps |
| Step | One action in a sequence, such as an email, wait period, call, or task |
| Enrollment | A prospect's active participation in a sequence |
| Template | Reusable email content with personalization variables |
| Sender mailbox | The connected Gmail or email account used for sending |
| Scheduled action | A step waiting to be executed at a future time |
| Activity | A historical record such as sent, opened, replied, failed, or paused |
| Campaign | A coordinated outreach effort for a particular audience or goal |

## Example sequence

```text
Day 1: Send introduction email
   ↓ wait 2 days
Day 3: Send follow-up if no reply
   ↓ wait 3 days
Day 6: Create a call task
   ↓ wait 2 days
Day 8: Send final follow-up if no reply
```

If the prospect replies, the remaining automated steps are commonly cancelled or paused.

---

# 3. High-Level Architecture

## Main components

```text
┌───────────────────────────────┐
│ Vue.js Web Application        │
│ Prospects, sequences, editor, │
│ scheduling and activity UI    │
└───────────────┬───────────────┘
                │ HTTPS / REST APIs
                ↓
┌───────────────────────────────┐
│ API Layer                     │
│ Authentication, validation,   │
│ authorization and workflows   │
└───────┬───────────┬───────────┘
        │           │
        ↓           ↓
┌──────────────┐  ┌──────────────────┐
│ MongoDB      │  │ Scheduler / Queue │
│ Application  │  │ Future actions    │
│ state        │  │ and retries       │
└──────────────┘  └────────┬─────────┘
                            ↓
                   ┌─────────────────┐
                   │ Email Workers    │
                   │ Compose and send │
                   └────────┬────────┘
                            ↓
                   ┌─────────────────┐
                   │ Gmail API       │
                   │ Send and sync    │
                   └────────┬────────┘
                            ↓
                   ┌─────────────────┐
                   │ Tracking / Sync │
                   │ Status, replies │
                   └────────┬────────┘
                            ↓
                   ┌─────────────────┐
                   │ Activity Store  │
                   │ and Analytics   │
                   └─────────────────┘
```

## Responsibilities

| Component | Responsibility |
|---|---|
| Vue.js application | User workflows, validation, editor, filters, and activity views |
| API layer | Authentication, authorization, validation, and business rules |
| MongoDB | Prospects, templates, sequences, enrollments, jobs, and activity records |
| Scheduler | Finds actions due for execution and places them on a queue |
| Queue | Buffers work, supports retry, and separates scheduling from sending |
| Email workers | Personalize content, apply limits, and call the provider API |
| Gmail integration | OAuth, email sending, thread metadata, and reply synchronization |
| Tracking pipeline | Processes delivery, engagement, reply, and failure events |

## End-to-end flow

```text
Representative creates prospect and sequence
                    ↓
Frontend validates and sends configuration
                    ↓
Backend stores sequence and enrollment
                    ↓
Scheduler creates or finds the next due action
                    ↓
Worker validates current state before execution
                    ↓
Email is personalized and sent through Gmail
                    ↓
Provider result and message identifiers are stored
                    ↓
Activity timeline is updated
                    ↓
Next step is scheduled, paused, or cancelled
```

---

# 4. Prospect Management

## Typical prospect information

- First and last name
- Email address
- Company and job title
- CRM contact or lead ID
- Owner
- Time zone
- Tags and custom fields
- Sequence enrollment status
- Last contacted date
- Latest activity and reply state
- Consent or suppression status

## Example data model

```json
{
  "id": "prospect_2041",
  "tenantId": "tenant_1007",
  "ownerId": "user_891",
  "crmContactId": "crm_contact_771",
  "email": "person@example.com",
  "firstName": "Asha",
  "lastName": "Rao",
  "company": "Example Corp",
  "timeZone": "Asia/Kolkata",
  "status": "active",
  "customFields": {
    "industry": "Software"
  },
  "createdAt": "2026-09-21T08:30:00Z"
}
```

## Important design decisions

### Duplicate prevention

A tenant may prevent duplicates using a normalized identifier such as:

```text
tenantId + normalizedEmail
```

A CRM contact ID is preferable when it is stable and consistently available. Email addresses can change, so the system may preserve both the internal ID and external CRM ID.

### Bulk import

For large CSV or CRM imports:

1. Upload and parse the file asynchronously.
2. Validate required fields.
3. Normalize email addresses and custom fields.
4. Detect duplicates and suppression-list entries.
5. Save valid records in batches.
6. Produce an import report for failed rows.

### Search and filtering

Common filters include owner, company, tag, sequence, enrollment state, last activity, and reply status. Large datasets should use server-side filtering, pagination, and indexed fields.

## Example APIs

```http
POST   /api/prospects
GET    /api/prospects?ownerId=...&status=...&cursor=...
GET    /api/prospects/:prospectId
PATCH  /api/prospects/:prospectId
POST   /api/prospects/imports
```

---

# 5. Sequence and Workflow Design

## Sequence model

```json
{
  "id": "sequence_3001",
  "tenantId": "tenant_1007",
  "name": "Enterprise introduction",
  "status": "active",
  "version": 4,
  "steps": [
    {
      "stepId": "step_1",
      "type": "email",
      "delayMinutes": 0,
      "templateId": "template_101"
    },
    {
      "stepId": "step_2",
      "type": "email",
      "delayMinutes": 2880,
      "templateId": "template_102",
      "condition": "no_reply"
    }
  ]
}
```

## Enrollment model

An enrollment is separate from the sequence definition because every prospect progresses independently.

```json
{
  "id": "enrollment_8001",
  "tenantId": "tenant_1007",
  "prospectId": "prospect_2041",
  "sequenceId": "sequence_3001",
  "sequenceVersion": 4,
  "currentStepIndex": 1,
  "status": "scheduled",
  "nextExecutionAt": "2026-09-23T04:30:00Z",
  "mailboxId": "mailbox_91"
}
```

## Why store the sequence version?

A sequence may be edited after prospects have already enrolled. Versioning provides predictable behavior:

- Existing enrollments can continue using the version they started with.
- New enrollments can use the latest version.
- An explicit migration can move existing enrollments when required.

Without versioning, editing a live sequence can unexpectedly change pending actions.

## Enrollment state machine

```text
draft
  ↓ activate
scheduled
  ↓ due
processing
  ├── success ──→ waiting_for_next_step
  │                   ↓
  │               scheduled
  ├── temporary failure ──→ retry_scheduled
  ├── permanent failure ──→ failed
  ├── prospect replied ───→ completed
  ├── user pauses ────────→ paused
  └── user removes ───────→ cancelled
```

All state transitions should be validated on the backend. The UI should not be the security or consistency boundary.

## Important workflow rules

- Do not send if the enrollment was paused or cancelled.
- Stop or pause automation when a qualifying reply is detected.
- Respect prospect and mailbox time zones.
- Respect weekends, business hours, holidays, and configured delays.
- Re-check suppression and consent immediately before sending.
- Prevent two active enrollments when the business rules prohibit them.
- Decide how live sequence edits affect existing enrollments.

## Example APIs

```http
POST   /api/sequences
PATCH  /api/sequences/:sequenceId
POST   /api/sequences/:sequenceId/activate
POST   /api/sequences/:sequenceId/enrollments
POST   /api/enrollments/:enrollmentId/pause
POST   /api/enrollments/:enrollmentId/resume
DELETE /api/enrollments/:enrollmentId
```

---

# 6. Email Composition and Templates

## Quill.js editor responsibilities

The rich-text editor can support:

- Text formatting
- Links and lists
- Personalization variables
- Signatures
- Templates
- Draft saving
- Previewing
- Content validation

## Personalization example

Template:

```text
Hi {{firstName}},

I noticed that {{company}} is expanding its revenue team.
Would you be available for a short conversation this week?
```

Resolved output:

```text
Hi Asha,

I noticed that Example Corp is expanding its revenue team.
Would you be available for a short conversation this week?
```

## Important design considerations

### Store source and rendered content separately

- The **template source** contains variables such as `{{firstName}}`.
- The **rendered snapshot** records exactly what was sent to a prospect.

Keeping the rendered snapshot is important because the template or prospect data may change later.

### Sanitize HTML

Rich-text HTML must be sanitized. Allow only supported tags and attributes, and prevent scripts, unsafe URLs, and unwanted styles.

### Email-client compatibility

Browser HTML does not render consistently in all email clients. Prefer simple markup, inline-compatible styling, and tested layouts.

### Validate personalization

Before sending:

- Resolve all supported variables.
- Detect missing required values.
- Apply approved fallback values.
- Avoid sending visible unresolved text such as `{{firstName}}`.

## Example send preview API

```http
POST /api/templates/:templateId/preview
```

```json
{
  "prospectId": "prospect_2041",
  "subject": "A quick question for {{company}}",
  "body": "<p>Hi {{firstName}}...</p>"
}
```

---

# 7. Email Scheduling and Execution

## Why scheduling belongs on the backend

The browser may close, lose connectivity, or run in a different time zone. The backend must own scheduled execution.

## Recommended high-level design

```text
Enrollment produces a scheduled action
                 ↓
Action stored with executeAt and status
                 ↓
Scheduler queries due actions in small batches
                 ↓
Actions are atomically claimed
                 ↓
Queue distributes jobs to email workers
                 ↓
Worker revalidates current business state
                 ↓
Worker sends through Gmail
                 ↓
Result is persisted and next step is scheduled
```

## Scheduled-action model

```json
{
  "id": "action_4009",
  "tenantId": "tenant_1007",
  "enrollmentId": "enrollment_8001",
  "stepId": "step_2",
  "executeAt": "2026-09-23T04:30:00Z",
  "status": "scheduled",
  "attemptCount": 0,
  "idempotencyKey": "enrollment_8001:step_2",
  "lockedAt": null,
  "lockedBy": null
}
```

Useful indexes include:

```text
(status, executeAt)
(tenantId, status, executeAt)
UNIQUE(idempotencyKey)
```

## Preventing duplicate sends

At-least-once queues may deliver a job more than once. Protection can include:

1. A unique idempotency key per enrollment step.
2. Atomic transition from `scheduled` to `processing`.
3. A send-attempt record created before calling Gmail.
4. Storage of the provider message ID after success.
5. State revalidation immediately before sending.

Exactly-once delivery is difficult across a database and external provider. The practical goal is an idempotent workflow that makes duplicate sends very unlikely and detectable.

## Handling edits and cancellation

When an enrollment is paused or cancelled:

- Mark future actions as cancelled.
- Let workers verify enrollment state before sending.
- Do not rely only on deleting queue messages because a worker may already have claimed one.

## Time-zone handling

Store absolute execution times in UTC. Calculate them using the prospect or mailbox time zone and the configured sending window.

```text
Prospect local target: Monday, 09:00 America/New_York
                         ↓
Convert to UTC when scheduling
                         ↓
Persist executeAt in UTC
                         ↓
Convert back only for display
```

---

# 8. Gmail Integration

## OAuth connection flow

```text
User clicks “Connect Gmail”
            ↓
Redirect to Google authorization
            ↓
User grants requested scopes
            ↓
Backend receives authorization code
            ↓
Backend exchanges code for tokens
            ↓
Refresh token is encrypted and stored
            ↓
Mailbox is ready for authorized operations
```

## Token handling

- Store refresh tokens only on the backend.
- Encrypt sensitive tokens at rest.
- Request the minimum required OAuth scopes.
- Never expose provider tokens to the browser.
- Refresh short-lived access tokens when required.
- Mark the mailbox as needing reconnection after revoked or invalid authorization.
- Maintain audit records for connection and disconnection.

## Send flow

```text
Worker loads mailbox connection
          ↓
Refreshes access token if required
          ↓
Builds MIME email with subject, HTML and headers
          ↓
Calls Gmail API
          ↓
Stores Gmail message ID and thread ID
          ↓
Creates a sent activity
```

## Gmail identifiers

| Identifier | Purpose |
|---|---|
| Internal send ID | Tracks the application's send attempt |
| Gmail message ID | Identifies the provider message |
| Gmail thread ID | Associates related messages in a conversation |
| RFC `Message-ID` header | Supports standard email threading and correlation |
| Enrollment and step IDs | Connect the message to the workflow |

## Rate limits and quotas

The provider may apply API and sending limits. The system should:

- Limit per-user and per-tenant concurrency.
- Apply backoff for quota-related failures.
- Spread scheduled work instead of sending large bursts.
- Respect provider and organizational sending policies.
- Show actionable status when a mailbox reaches a limit.

---

# 9. Email and Reply Tracking

## Tracking events

Possible activities include:

- Scheduled
- Sent
- Delivery failed or bounced
- Opened
- Link clicked
- Replied
- Unsubscribed or suppressed

Do not promise that every email provider supplies every event. The available signals depend on the integration and tracking mechanism.

## Open tracking

A common method inserts a tiny unique image URL:

```html
<img src="https://tracking.example.com/open/send_9001.gif" width="1" height="1" alt="">
```

When an email client requests the image, the tracking service records an open event.

Limitations:

- Image caching can create misleading results.
- Privacy protection may preload images.
- Some clients block remote images.
- Multiple opens may not represent multiple reads.

An open event is an approximate engagement signal, not guaranteed proof that a human read the email.

## Click tracking

Original link:

```text
https://customer.example.com/demo
```

Tracked link:

```text
https://tracking.example.com/click/send_9001/link_2
```

The tracking service records the event and redirects to the original URL. Redirect targets must be validated to avoid creating an open-redirect vulnerability.

## Reply synchronization

Replies can be detected using provider notifications, history synchronization, or periodic polling.

```text
Mailbox changes
      ↓
Provider notification or polling
      ↓
Fetch messages after last stored history position
      ↓
Correlate using thread ID, message headers and participants
      ↓
Create reply activity
      ↓
Pause or complete active enrollment
```

Store a synchronization cursor or history ID so processing can resume incrementally. Periodic reconciliation protects against missed notifications.

## Event deduplication

A unique key can include:

```text
tenantId + provider + providerEventId
```

If the provider does not supply a stable event ID, derive a deterministic key from the message, event type, and provider timestamp where safe.

---

# 10. Activity Timeline

The activity timeline gives the representative a chronological view of prospect engagement and workflow execution.

## Example record

```json
{
  "id": "activity_7701",
  "tenantId": "tenant_1007",
  "prospectId": "prospect_2041",
  "enrollmentId": "enrollment_8001",
  "type": "email_sent",
  "source": "gmail",
  "occurredAt": "2026-09-21T08:32:00Z",
  "metadata": {
    "messageId": "gmail_message_881",
    "threadId": "gmail_thread_501",
    "stepId": "step_1"
  }
}
```

## Design recommendations

- Treat activities as append-only facts when possible.
- Store provider and internal identifiers for traceability.
- Index by tenant, prospect, and occurrence time.
- Paginate long timelines.
- Use a consistent event vocabulary.
- Separate raw provider events from normalized product activities.

---

# 11. Reliability and Failure Handling

## Failure categories

| Category | Examples | Handling |
|---|---|---|
| Validation | Missing recipient, unresolved variable | Fail without retry; ask user to correct data |
| Authentication | Revoked OAuth token | Mark mailbox disconnected; request reconnection |
| Rate limiting | Provider quota exceeded | Retry with exponential backoff and jitter |
| Temporary provider error | Timeout or HTTP 5xx | Retry with a bounded attempt count |
| Permanent provider error | Invalid recipient or rejected message | Mark failed; do not retry blindly |
| Internal failure | Worker crash after claiming job | Release expired lock or retry from queue |

## Retry strategy

```text
Attempt 1 fails temporarily
        ↓
Retry after 1 minute
        ↓
Retry after 5 minutes
        ↓
Retry after 30 minutes
        ↓
Maximum attempts reached
        ↓
Dead-letter queue and visible failure state
```

Add jitter so many failed jobs do not retry simultaneously.

## Outbox pattern

If a database update must reliably produce a queue event, store both the business change and an outbox record in one database transaction. A separate publisher sends unsent outbox records to the queue.

```text
Database transaction
  ├── update enrollment
  └── insert outbox event
              ↓
Outbox publisher
              ↓
Queue
              ↓
Worker
```

This prevents a state where the database commits successfully but the process crashes before publishing the event.

## Main challenge answer

> One of the main challenges was coordinating asynchronous operations such as scheduling, sending, and activity updates. A user could modify a sequence, an email-provider request could fail, or a job could be delivered more than once.
>
> The system therefore needed clear workflow states, backend validation, retry handling, and a way to prevent duplicate sends. Before executing a job, the worker should re-check the enrollment, suppression, mailbox, and action states. A unique key per enrollment step can make repeated processing safe.

Use the term **idempotent processing** only if the actual implementation supported it. Otherwise, describe it as an improvement you would recommend.

---

# 12. Security and Authorization

## Important controls

- Authenticate every API request.
- Authorize access by tenant, role, owner, and resource.
- Enforce permissions on the backend, not only in the UI.
- Encrypt OAuth refresh tokens and other secrets.
- Request minimal Gmail scopes.
- Sanitize rich-text HTML.
- Protect OAuth callbacks with state validation.
- Validate webhook signatures or source authenticity.
- Maintain audit logs for sensitive actions.
- Apply rate limits to public and expensive endpoints.
- Prevent cross-tenant queries by requiring `tenantId` in every data-access path.

## Example roles

| Role | Typical access |
|---|---|
| Sales representative | Own prospects, sequences, mailbox, and activities |
| Manager | Team-level prospects, sequences, analytics, and controls |
| Administrator | Tenant configuration, integrations, policies, and users |

## Suppression and compliance

Before sending, check whether the prospect is:

- Unsubscribed
- On a global or tenant suppression list
- Missing required consent under applicable rules
- Associated with a blocked domain
- Already contacted beyond configured frequency limits

Legal and compliance rules depend on jurisdiction and company policy; they should be implemented with appropriate legal guidance.

---

# 13. Performance and Scalability

## Frontend performance

- Use server-side pagination and filtering for large prospect tables.
- Debounce search requests.
- Virtualize large lists or grids.
- Lazy-load heavy editors and analytics views.
- Avoid storing unnecessary large payloads in Vuex.
- Update only affected prospects and activities after an operation.
- Cancel obsolete requests when filters change quickly.
- Cache stable reference data.

## Backend performance

- Index tenant and query fields.
- Use cursor-based pagination for frequently changing datasets.
- Batch independent database operations where safe.
- Keep provider calls outside long database transactions.
- Cache stable configuration and template metadata.
- Avoid scanning all scheduled actions; query indexed due records.
- Move expensive imports, tracking events, and sends to workers.

## Scaling workers

Email workers can scale horizontally because work is distributed through a queue. Concurrency must still respect:

- Per-mailbox provider limits
- Per-tenant limits
- Global API quotas
- Fairness between tenants
- Database and queue capacity

Partitioning or routing jobs by mailbox can preserve per-mailbox ordering when required.

## Backpressure

If the provider slows down, the queue absorbs temporary load. The system should monitor queue age and depth, reduce producer rate when necessary, and prevent unbounded growth.

## Capacity-estimation example

Suppose:

```text
100,000 active enrollments
Average 3 email steps per enrollment
300,000 emails per campaign lifecycle
20% scheduled during the busiest hour
60,000 sends/hour ≈ 17 sends/second
```

Then add retry traffic and safety margin before deciding worker count. Provider quotas may be a tighter constraint than CPU capacity.

---

# 14. Monitoring and Testing

## Useful metrics

- Scheduled actions due
- Queue depth and oldest-job age
- Send throughput
- Success, retry, and permanent-failure rates
- Gmail API latency and error rate
- OAuth reconnection rate
- Duplicate-send prevention count
- Reply-sync lag
- Webhook or history-sync failures
- Sequence completion and reply rates

## Useful logs and tracing fields

Include identifiers such as:

```text
requestId
tenantId
prospectId
sequenceId
enrollmentId
actionId
mailboxId
providerMessageId
```

Do not log access tokens or complete sensitive email content unnecessarily.

## Alerts

Create alerts for conditions such as:

- Queue age above the expected scheduling tolerance
- Sudden increase in send failures
- Provider rate-limit spike
- Reply synchronization falling behind
- Repeated worker crashes
- Dead-letter queue growth
- Abnormal activity drop for a tenant

## Testing strategy

### Unit tests

- Personalization-variable resolution
- State-transition validation
- Send-window and time-zone calculations
- Retry classification
- Permission checks

### Integration tests

- API and MongoDB behavior
- OAuth token refresh
- Queue producer and consumer behavior
- Provider error mapping
- Reply correlation

### End-to-end tests

- Create prospect and sequence
- Enroll prospect
- Schedule and send a test message
- Record activity
- Detect reply
- Stop remaining sequence steps

### Failure tests

- Duplicate queue delivery
- Worker crash during execution
- Expired or revoked OAuth token
- Provider timeout
- Missed webhook followed by reconciliation
- Sequence paused while a job is waiting

---

# 15. Common Interview Questions

## Why use a queue?

> Email sending is asynchronous, can experience provider failures, and may need retry or rate limiting. A queue separates user-facing APIs from background execution, absorbs traffic spikes, distributes work across workers, and allows controlled retries.

## Why not schedule emails in the browser?

> The browser may close, lose connectivity, or use an incorrect local time. The backend must own execution so scheduled work remains reliable and auditable.

## How do you prevent duplicate emails?

> Give every enrollment step a unique idempotency key, atomically claim scheduled work, re-check current state before sending, and store send attempts and provider message IDs. If the same job is delivered again, the worker can detect that the step was already processed.

## How do you handle a prospect reply?

> Synchronize mailbox changes through provider notifications or polling, correlate the incoming message using thread and message identifiers, record a reply activity, and pause or complete the active enrollment according to the sequence rules.

## What if a sequence changes after enrollment?

> Version the sequence. Existing enrollments can remain on their original version, while new enrollments use the latest version. If existing enrollments must change, perform an explicit migration with clear rules for pending steps.

## How do you handle time zones?

> Calculate the intended send time using the configured prospect or mailbox time zone and business-hour rules, convert it to UTC, store it as an absolute timestamp, and convert it back only for display.

## How do you secure Gmail integration?

> Use OAuth, request minimal scopes, store refresh tokens only on the backend, encrypt them at rest, protect the OAuth callback, never expose tokens to the browser, and require reconnection when authorization is revoked.

## How do you debug a scheduled email that was not sent?

Check the flow in order:

1. Was the enrollment active?
2. Was a scheduled action created with the correct UTC time?
3. Did the scheduler find and claim it?
4. Was the job added to the queue?
5. Did a worker receive it?
6. Did pre-send validation block it?
7. Was the mailbox authorized and under its quota?
8. What response came from Gmail?
9. Was a retry or failure activity recorded?

Use `enrollmentId`, `actionId`, and provider identifiers to trace the complete path.

## What would you improve?

> I would strengthen observability across the complete scheduling and sending path, make every workflow step safely idempotent, use sequence versioning for predictable edits, add reconciliation for missed provider events, and expose clear failure reasons so users can correct problems without engineering support.

---

# 16. Sales Engagement versus Customer Success Intelligence

| Project | Primary user | Main objective | Main system characteristic |
|---|---|---|---|
| Sales Engagement | Sales representatives | Engage prospects and manage outreach | Workflow and communication oriented |
| Customer Success Intelligence | Customer Success Managers | Monitor customers and identify risks | Data aggregation and analytics oriented |

## Interview answer

> Sales Engagement focuses on helping sales representatives acquire and engage prospects through structured outreach. Customer Success Intelligence focuses on helping Customer Success Managers understand and retain existing customers by monitoring health, usage, support activity, and engagement.
>
> Sales Engagement is primarily workflow- and communication-oriented, while Customer Success Intelligence is primarily data-aggregation, monitoring, and analytics-oriented.

## Combined résumé-style answer

> At Aviso AI, I contributed to two major product areas: Sales Engagement and Customer Success Intelligence.
>
> In Sales Engagement, I worked on prospect management, email sequences, scheduling, rich-text email composition, Gmail integration, activity tracking, and campaign workflows.
>
> In Customer Success Intelligence, I worked on unified account dashboards, customer-health insights, support-ticket tracking, product-usage analytics, configurable views, data visualization, and role-based access control.
>
> Across both products, I developed frontend features using Vue.js and React.js, integrated REST APIs, contributed to backend services using Express.js and FastAPI, worked with MongoDB, optimized performance, and resolved production issues.

---

# Final Preparation Checklist

Before using these answers in an interview, replace generic design details with facts from your implementation:

- Which screens and components did you personally build?
- Did the system support multi-step sequences or only scheduled emails?
- Which Gmail APIs and OAuth scopes were used?
- How were jobs actually scheduled and executed?
- Was a message queue used? Which one?
- How were duplicate sends prevented?
- How were replies synchronized and correlated?
- Were open and click tracking implemented?
- Which statuses existed in the real workflow?
- What volume of prospects and emails did the system handle?
- What performance or production issue did you personally solve?
- How was the reported productivity or response-rate improvement measured?

When you did not directly own a component, say:

> I did not directly implement that component, but my understanding of the system flow is...

When describing a proposed improvement, say:

> The implementation I would recommend is...
