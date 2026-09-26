# Sales Engagement — Quick Interview Notes

## Simple project description

> Sales Engagement helps sales representatives organize prospect outreach. They can manage prospects, create reusable templates and sequences, enroll prospects, and view all engagement activities from one place.

## My contribution

> I worked on prospect-management screens, template and sequence workflows, Quill.js editor integration, activity views, REST API integration, Vuex state management, and responsive UI development.

Mention only the features you actually worked on.

---

## Important terms

| Term | Meaning |
|---|---|
| Prospect | A person the sales representative wants to contact |
| Template | Reusable personalized content |
| Sequence | Outreach steps arranged in order with time gaps |
| Enrollment | Adding a prospect to a sequence |
| Activity | A record of what happened for a prospect |

---

## High-level design

```text
Sales representative
        ↓
Vue.js frontend
        ↓ REST APIs
Express.js backend
        ↓
MongoDB
        ↓
Activity timeline and reports
```

- **Vue.js:** prospect, template, sequence, and activity screens
- **Vuex:** shared frontend state
- **Express.js:** validation and business logic
- **MongoDB:** prospects, templates, sequences, enrollments, and activities

---

## 1. Prospect management

Users can:

- Add and update prospects
- Search and filter prospects
- Group prospects using tags or lists
- View prospect activities
- Add prospects to a sequence

Example APIs:

```http
POST  /api/prospects
GET   /api/prospects
PATCH /api/prospects/:id
```

Use server-side pagination and filtering when the prospect list is large.

---

## 2. Templates and personalization

The frontend can use **Quill.js** as a rich-text editor.

```text
Hi {{firstName}},

I would like to discuss how we can help {{company}}.
```

The backend replaces variables using prospect information:

```text
Hi Asha,

I would like to discuss how we can help ABC Ltd.
```

Before using the content:

- Validate missing variables.
- Sanitize the HTML.
- Store the template separately from the final personalized content.

---

## 3. Sequences

A sequence contains multiple outreach steps:

```text
Step 1: Introduction
Step 2: Follow-up after 2 days
Step 3: Final reminder after 3 more days
```

When a prospect is enrolled:

1. Create an enrollment record.
2. Calculate the time for each step.
3. Track the current step and enrollment status.
4. Stop remaining steps if the prospect replies, unsubscribes, or the sequence is paused.

Example enrollment:

```json
{
  "prospectId": "prospect_101",
  "sequenceId": "sequence_501",
  "currentStep": 1,
  "status": "active"
}
```

---

## 4. Activity timeline

The activity timeline gives one view of everything that happened for a prospect.

```text
PROSPECT_CREATED
SEQUENCE_ENROLLED
STEP_COMPLETED
CUSTOMER_REPLIED
SEQUENCE_PAUSED
```

Each activity should contain:

```text
tenantId + prospectId + activityType + occurredAt
```

---

## Detailed email notes

Email scheduling, Gmail APIs, tracking, and synchronization are explained separately:

[Email Scheduling and Tracking](./emailSchedulingTracking.md)

Gmail authentication and token storage are explained here:

[Gmail OAuth 2.0 Integration](./gmailOAuthIntegration.md)

---

## Interview answer

> Sales Engagement helps sales representatives manage prospects and organize outreach. The frontend was built with Vue.js and Vuex, while Express.js and MongoDB handled APIs and business data.
>
> Users could manage prospects, create reusable templates, personalize content, build multi-step sequences, enroll prospects, and view an activity timeline. My work included prospect and sequence workflows, Quill.js editor integration, Vuex state management, REST API integration, and responsive UI development.
>
> One important part was keeping prospect, enrollment, and activity states consistent. We used backend validation, clear statuses, and stable identifiers so the UI always showed the latest sequence progress.

## Short answer

> Sales Engagement helps representatives manage prospects, build personalized outreach sequences, track enrollment progress, and view prospect activities from one place.
