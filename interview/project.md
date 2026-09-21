# Aviso AI Project Interview Notes

Use this document to prepare explanations for the following projects and modules:

1. [Customer Success Intelligence](#1-customer-success-intelligence)
2. [Product usage tracking](#2-product-usage-tracking)
3. [Account health scoring](#3-account-health-scoring)
4. [Support-ticket synchronization](#4-support-ticket-synchronization)
5. [Deals module](#5-deals-module)
6. [Forecasting module](#6-forecasting-module)
7. [Deals versus Forecasting](#7-deals-versus-forecasting)

# 1. Customer Success Intelligence

## One-line description

> Customer Success Intelligence is a unified analytics platform that helps Customer Success Managers monitor customer health, product usage, support activity, and engagement so they can identify risks(identify accounts requiring attention) and take proactive action.

## Interview-ready explanation

> At Aviso AI, I worked on a Customer Success Intelligence platform designed to help Customer Success Managers monitor customer health and manage accounts proactively.
>
> Customer information—such as product usage, support tickets, engagement activities, account details, and business metrics—often exists across multiple systems. The platform brings this information into a unified dashboard so CSMs can understand account health, identify risk, and prioritize customer engagement.
>
> I contributed to interactive dashboards, ticket tracking, global search, advanced filters, and configurable data views. I also integrated backend services and APIs to present customer data in a consistent format.
>
> On the frontend, I primarily used Vue.js to build reusable components, tables, charts, and responsive interfaces. On the backend, I worked with Express.js and MongoDB-based services for data retrieval, aggregation, and synchronization.
>
> I also contributed to role-based access control so users could access only permitted accounts and actions. For performance, I worked on reducing unnecessary API requests, optimizing component rendering, and efficiently handling large datasets.

## My role

> My responsibility was to develop and integrate end-to-end features across dashboards, account management, ticket tracking, search, filtering, configurable views, data visualization, API integration, access control, and performance optimization.

## High-level technical flow

Backend services collect information from internal and external sources, normalize it, and expose application-oriented APIs. The frontend presents this information through account summaries, KPIs, tables, charts, and activity views.

```text
Product telemetry, CRM, support and engagement data
                         ↓
              Backend services and APIs
                         ↓
             Aggregation and normalization
                         ↓
                  Frontend state
                         ↓
          KPIs, tables, charts and account views
                         ↓
            Customer Success Manager action
```

Independent datasets can be loaded in parallel. Each dashboard section should have its own loading and error state so one slow service does not block the entire page.

## Main challenge

> One of the main challenges was presenting data from multiple sources while keeping the dashboard accurate and responsive. Different services could have different response times, formats, or missing data.
>
> We handled this through clear API contracts, normalized response models, parallel loading of independent data, section-level loading and error states, fewer duplicate requests, and optimization of expensive tables and visualizations.

---

# 2. Product Usage Tracking

## What is measured?

Product usage measures how actively and successfully a customer uses the product. Typical signals include:

- Daily, weekly, and monthly active users
- Login frequency
- Licensed users versus active users
- Adoption of important features
- Actions or workflows completed
- Last activity date
- Usage growth or decline
- Adoption across teams or departments
- Consumption against purchased limits
- Errors, failed operations, and abandoned workflows

## Usage-event example

When a user performs an important action, the frontend or backend generates a usage event:

```json
{
  "eventId": "evt_78321",
  "tenantId": "tenant_1007",
  "accountId": "account_245",
  "userId": "user_891",
  "eventName": "forecast_submitted",
  "timestamp": "2026-09-21T08:30:00Z",
  "properties": {
    "module": "forecasting",
    "source": "web"
  }
}
```

## Processing flow

```text
User performs an action
        ↓
Frontend or backend creates a usage event
        ↓
Event collector, queue, or analytics service
        ↓
Validation and deduplication
        ↓
Daily or weekly account-level aggregation
        ↓
Customer Success Intelligence API
        ↓
Account dashboard and health-score calculation
```

Raw events can be aggregated into an account summary:

```json
{
  "accountId": "account_245",
  "weeklyActiveUsers": 84,
  "licensedUsers": 120,
  "weeklyActiveUserRate": 70,
  "keyFeatureAdoptionRate": 62,
  "usageTrendPercentage": -8,
  "lastActivityAt": "2026-09-21T08:30:00Z"
}
```

The dashboard reads aggregated metrics rather than processing millions of raw events in the browser. This keeps API payloads and frontend rendering manageable.

## Engineering considerations

- Give every event a unique `eventId` for deduplication.
- Include `tenantId` to isolate data belonging to different customers.
- Store timestamps in UTC and convert them only for display.
- Govern and version event names and schemas.
- Exclude internal users, test accounts, and bots when appropriate.
- Do not automatically interpret missing telemetry as poor usage.
- Use consistent time windows when comparing current and previous periods.

## Interview answer

> We tracked meaningful customer actions as product-usage events. Each event contained identifiers such as the tenant, account, user, event type, and timestamp. Backend pipelines validated and aggregated these events into metrics such as active-user rate, feature adoption, usage frequency, and usage trends.
>
> The Customer Success dashboard consumed aggregated account-level metrics and displayed them through KPIs and charts. These metrics could also become inputs to the account health score.

---

# 3. Account Health Scoring

## Definition

An account health score summarizes the overall condition of a customer account. It helps a Customer Success Manager identify healthy accounts and prioritize accounts that need attention.

## Possible inputs

| Category | Example signals |
|---|---|
| Product adoption | Active-user rate, key-feature adoption, usage trend |
| Engagement | Meetings, emails, response rate, executive engagement |
| Support | Open tickets, critical tickets, ticket age, escalations |
| Commercial | Renewal date, contract value, payment status, expansion |
| Sentiment | Survey score, call or email sentiment, CSM assessment |
| Relationship | Active stakeholders and decision-maker engagement |

## Example weighted formula

Normalize every category to a value between 0 and 100, then apply configurable weights:

```text
Health score =
    Product adoption score × 40%
  + Engagement score       × 20%
  + Support score          × 20%
  + Commercial score       × 10%
  + Sentiment score        × 10%
```

Example:

```text
Product adoption = 80 × 0.40 = 32
Engagement       = 65 × 0.20 = 13
Support          = 50 × 0.20 = 10
Commercial       = 90 × 0.10 =  9
Sentiment        = 70 × 0.10 =  7
                                 --
Final health score              = 71/100
```

Example status thresholds:

| Score | Status | Meaning |
|---:|---|---|
| 75–100 | Green | Healthy |
| 50–74 | Amber | Needs attention |
| 0–49 | Red | At risk |

The metrics, weights, and thresholds are examples. A real implementation commonly makes them configurable by customer, segment, product, or account type.

## Rule-based versus model-based scoring

### Rule-based score

Business teams define metrics, weights, thresholds, and penalties. This approach is transparent and easy to explain.

### Model-based score

A statistical or machine-learning model learns which signals correlate with churn, renewal, or expansion.

A platform can combine both methods—for example, showing a configurable business health score alongside an AI-generated risk prediction.

## Example support adjustments

```text
Open critical ticket older than 48 hours:  -15
Three or more escalated tickets:           -10
Ticket volume increased by over 50%:        -5
All critical tickets resolved:              +5
```

Avoid penalizing the same underlying issue multiple times unless that behavior is intentional.

## Handling missing data

Missing information should not automatically become zero because zero represents poor performance, while missing means unknown.

A safer approach is to:

- Mark the component as unavailable.
- Rebalance remaining weights where appropriate.
- Display data completeness or confidence.
- Temporarily preserve the previous score if a source is delayed.
- Explain which inputs caused the latest score change.

## Interview answer

> The account health score provides a consolidated view of customer risk. It can combine normalized signals from product adoption, engagement, support tickets, commercial information, and sentiment.
>
> Each category receives a configurable weight, and the final score is mapped to a status such as healthy, needs attention, or at risk. The interface should also explain the factors behind the score so a CSM can understand and act on it instead of seeing only an unexplained number.

---

# 4. Support-Ticket Synchronization

Support tickets may originate in systems such as Zendesk, Jira Service Management etc.

## Synchronization strategies

### Initial and scheduled synchronization

The integration periodically requests tickets created or updated after the previous successful synchronization:

```http
GET /tickets?updated_after=<last_successful_sync_time>
```

This supports:

- Initial historical import
- Recovery of events missed during downtime
- Reconciliation of inconsistent records
- Integrations that do not provide webhooks

### Real-time webhook synchronization

```text
Ticket is created or updated
        ↓
Provider sends a webhook
        ↓
Integration authenticates and validates it
        ↓
Event enters a queue
        ↓
Worker maps and upserts the ticket
        ↓
Account metrics and health score are refreshed
```

A robust design commonly uses both:

- **Webhooks** for low-latency updates
- **Incremental synchronization** for recovery and reconciliation

## Which identifiers are required?

Ticket synchronization has two separate identity problems:

1. How do we uniquely identify the ticket?
2. How do we associate it with the correct customer account?

### Ticket identity

Use a composite key:

```text
tenantId + sourceSystem + externalTicketId
```

Example:

```json
{
  "tenantId": "tenant_1007",
  "sourceSystem": "zendesk",
  "externalTicketId": "987654",
  "internalTicketId": "ticket_abc123"
}
```

`externalTicketId` alone may not be globally unique because separate customers or support systems can use the same numeric ID.

The database can enforce:

```sql
UNIQUE (tenant_id, source_system, external_ticket_id)
```

Synchronization then performs an upsert:

```text
Ticket exists         → update changed fields
Ticket does not exist → insert a new record
```

### Account identity

The preferred solution is a stable mapping created during integration setup:

```text
Internal account ID ↔ CRM account ID ↔ Support organization ID
```

Example:

```json
{
  "tenantId": "tenant_1007",
  "internalAccountId": "account_245",
  "crmAccountId": "0018X00002ABCDQ",
  "supportOrganizationId": "zendesk_org_741"
}
```

A ticket with `supportOrganizationId = zendesk_org_741` can then be connected reliably to `account_245`.

### Account-matching keys in preferred order

1. Support-system organization ID mapped to the internal account ID
2. CRM account ID stored in the support system
3. Verified customer or tenant ID in a custom ticket field
4. Verified email domain
5. Requester email mapped to an existing contact

Email domain should be a fallback because:

- One company may use several domains.
- Separate companies may share public email domains.
- Consultants may submit tickets for customers.
- A company may change its domain.
- Subsidiaries may require separate account records.

If no reliable match exists, place the ticket in an unmatched queue instead of silently assigning it to the wrong account.

## Normalized ticket record

```json
{
  "id": "ticket_abc123",
  "tenantId": "tenant_1007",
  "accountId": "account_245",
  "sourceSystem": "zendesk",
  "externalTicketId": "987654",
  "status": "open",
  "priority": "high",
  "subject": "Unable to publish forecast",
  "requesterId": "contact_55",
  "createdAt": "2026-09-20T04:15:00Z",
  "updatedAt": "2026-09-21T06:40:00Z",
  "resolvedAt": null,
  "sourceUpdatedAt": "2026-09-21T06:40:00Z"
}
```

## Preventing duplicate and stale updates

- Enforce a unique composite key for each external ticket.
- Use upserts instead of unconditional inserts.
- Store the provider's `updatedAt` value or version number.
- Ignore an event older than the version already stored.
- Store webhook event IDs to detect repeated delivery.
- Make consumers idempotent so retries are safe.
- Use retry queues and a dead-letter queue for repeated failures.
- Periodically reconcile local data with the source system.

## Update flow

```text
Support system sends an update
        ↓
Find ticket using tenant + source + external ticket ID
        ↓
Compare source version or updated timestamp
        ↓
Normalize status, priority and timestamps
        ↓
Upsert ticket
        ↓
Recalculate account support metrics
        ↓
Recalculate or invalidate health score
        ↓
Refresh dashboard or publish an update event
```

Health-score calculation does not need to happen inside the webhook request. A safer design acknowledges the webhook quickly, queues the work, and updates the ticket and score asynchronously.

## Interview answer

> Support tickets are synchronized from an external ticketing system through webhooks, incremental polling, or both. We uniquely identify a ticket using the tenant, source system, and external ticket ID.
>
> To associate the ticket with a customer, we preferably maintain a mapping between the support-system organization ID and our internal account ID. CRM account IDs or verified tenant identifiers can also be used, while email domains are only a fallback.
>
> Updates are processed as idempotent upserts. We compare source timestamps or versions to prevent stale updates and periodically reconcile records so a missed webhook does not cause permanent inconsistency.

## Complete Customer Success answer

> In Customer Success Intelligence, we bring together product usage, support information, engagement, and commercial data to give CSMs a unified account view.
>
> For product usage, meaningful actions generate events containing the tenant, account, user, event type, and timestamp. Backend pipelines aggregate these events into metrics such as active-user rate, key-feature adoption, usage frequency, and usage trends. The dashboard consumes aggregated metrics instead of processing raw events directly.
>
> The account health score combines normalized signals from product adoption, engagement, support tickets, commercial status, and sentiment. These signals can have configurable weights, and the result is mapped to statuses such as healthy, needs attention, or at risk. The dashboard also explains the factors behind the score and distinguishes missing data from poor performance.
>
> For support tickets, we can integrate with systems such as Zendesk or ServiceNow using webhooks for real-time changes and incremental polling for recovery and reconciliation. A ticket is uniquely identified using the tenant ID, source system, and external ticket ID. A stable support-organization or CRM-account mapping connects it to the correct account. Idempotent upserts prevent duplicate webhook deliveries from creating duplicate tickets. After ticket metrics change, the account summary and health score can be refreshed asynchronously.

### Short version

> We collect product telemetry and aggregate it into adoption metrics, combine those metrics with engagement, support, and commercial signals to calculate a configurable account health score, and synchronize support tickets using webhooks plus scheduled reconciliation. A composite external identifier uniquely identifies each ticket, while a support-organization-to-account mapping connects it to the correct customer.

---

# 5. Deals Module

## Simple definition

> The Deals module helps sales teams inspect individual opportunities, understand their health and progress, identify risks, and decide the next action required to move them toward closure.

## Interview-ready explanation

> At Aviso AI, I worked on the Deals module, which gives sales representatives and managers a centralized view of their sales opportunities.
>
> The module brings together CRM information such as account, deal owner, amount, stage, forecast category, expected close date, activities, engagement signals, and deal history. It helps users understand which deals are progressing normally, which are at risk, and which require immediate attention.
>
> Users can search, filter, sort, group, and configure their deal views. They can inspect an individual opportunity, review recent activity, identify changes in stage or close date, and take appropriate next actions. The platform can also surface intelligence such as deal risk, AI-generated WinScore, stalled opportunities, engagement signals.

>
> I contributed to frontend workflows, configurable data views, filters, analytics visualizations, API integration, performance improvements, and production issue resolution. I worked with Vue.js, Vuex, microfrontends, Express.js, Redis, and MongoDB.
>
> One important challenge was displaying a large and frequently changing collection of opportunities without slowing down the UI. We addressed this through techniques such as pagination or virtualization, optimized state updates, reusable components, lazy loading, and fewer unnecessary API requests and rerenders.

## Typical deal information

- Account and opportunity name
- Deal owner and sales team
- Deal amount
- Current stage
- Forecast category
- Expected close date
- Probability or AI WinScore
- Recent calls, meetings, and emails
- Customer engagement
- Deal risks and warnings
- Next steps
- Historical field changes

## Technical flow

```text
CRM and engagement data
          ↓
Backend synchronization and processing
          ↓
Deal intelligence and risk calculation
          ↓
Deals APIs
          ↓
Vue.js deal-list and detail views
          ↓
Sales representative or manager action
```

## My contribution

> My work focused on presenting complex deal data through usable and performant interfaces. I contributed to deal-list views, filtering, sorting, configurable columns, deal-detail workflows, analytics, and API integration.
>
> I also worked on production issues, customer-specific edge cases, and performance problems caused by large datasets or unnecessary component updates.

## Technical challenges

### Large datasets

>  processing the complete dataset on the client could make the screen slow. We used approaches such as server-side pagination, virtualized rows, debounced filters, efficient lookup structures, and loading only the data needed for the current view.

### Dynamic configuration

> Different customers and roles could require different fields and views. We therefore needed configurable columns, filters, and permissions without creating a separate implementation for every customer.

### Data consistency

> Deal data could change in the CRM or through another application workflow. The UI needed to display the latest information while preventing conflicting or stale updates.

---

# 6. Forecasting Module

## Simple definition

> The Forecasting module helps revenue teams predict how much business will close, understand the deals behind that prediction, and compare salesperson judgment with AI-driven estimates.

## Interview-ready explanation

> At Aviso AI, I worked on the Forecasting module, which helps sales representatives, managers, and revenue leaders estimate how much revenue is likely to close during a selected period.
>
> The module combines opportunity data, sales-representative submissions, historical trends, pipeline movement, and AI predictions. It presents forecast values at different hierarchy levels, such as representative, manager, region, team, and organization.
>
> A representative can submit a forecast based on the deals they expect to close. Managers can review those submissions, inspect the underlying opportunities, compare human judgment with AI predictions, and roll the values up through the organizational hierarchy.
>
> The module commonly presents categories such as commit, best case, pipeline, and closed. It can also show quota attainment, pipeline coverage, changes from previous submissions, pacing, and the deals affecting the forecast.
>
> I contributed to forecasting interfaces, hierarchical data views, analytics visualizations, configurable tables, API integration, and performance improvements. I also worked on production issues and helped make the codebase more modular through microfrontends and the Vue 2-to-Vue 3 migration.
>
> A major challenge was presenting aggregated data across multiple hierarchy levels while allowing users to drill down to individual deals. We had to manage large datasets, complex filters, permissions, and forecast changes without losing context.

## Common forecast categories

The exact categories vary by organization:

- **Closed:** Revenue already won during the period
- **Commit:** Deals the sales team strongly expects to close
- **Best case:** Revenue that may close under favorable conditions
- **Pipeline:** Relevant open opportunities
- **AI forecast:** A system-generated prediction based on deal and historical signals

## Hierarchy and drill-down

```text
Organization forecast
        ↓
Region or business unit
        ↓
Sales manager
        ↓
Sales representative
        ↓
Individual deals
```

A senior leader can start from the organization forecast and drill down to the individual opportunities causing a change.

## Conceptual example

```text
Closed revenue       = ₹40 crore
Committed revenue    = ₹25 crore
Best-case revenue    = ₹15 crore
Remaining pipeline   = ₹30 crore
```

These values answer different questions:

- What has already closed?
- What is the team confident about?
- What could close under favorable conditions?
- What additional pipeline is available?
- What does the AI predict from current evidence?

Do not imply that the final forecast is calculated by simply adding these categories. Actual forecast logic varies by customer and model.

## Forecast-submission flow

```text
Sales representative reviews deals
                ↓
Representative submits forecast
                ↓
Manager reviews submission
                ↓
Manager adjusts or rolls up forecast
                ↓
Regional and organizational aggregation
                ↓
Leadership compares human and AI forecasts
```

## My contribution

> I worked on frontend features for displaying and managing forecast data, including hierarchical tables, filters, summary metrics, charts, drill-down interactions, configurable views, and forecasting API integration.
>
> I also helped improve performance by reducing unnecessary rendering, optimizing data transformations, applying lazy loading and code splitting, and investigating slow APIs or large payloads.

## Technical challenges

### Hierarchical aggregation

> A forecast screen must display values at different levels while keeping parent totals consistent with child data. Changes at the representative or deal level may affect manager and organizational totals.

### Human versus AI values

> The interface must clearly distinguish user-submitted forecasts from AI predictions. Users should understand which value they entered, which value the system predicted, and which deal-level signals explain the difference.

### Historical comparison

> The module may compare the current forecast with previous weeks or quarters. This requires preserving forecast snapshots and aligning data across different time periods.

### Permissions

> A representative generally sees their own scope, while managers and leaders require visibility into larger parts of the hierarchy. Frontend visibility and backend authorization must both enforce this correctly.

---

# 7. Deals versus Forecasting

| Deals module | Forecasting module |
|---|---|
| Focuses on individual opportunities | Focuses on expected revenue |
| Inspects deal health and activity | Estimates period-level outcomes |
| Answers, “What is happening with this deal?” | Answers, “How much are we likely to close?” |
| Shows risks, engagement, and next actions | Shows commit, best case, attainment, and AI prediction |
| Primarily operational | Primarily planning and decision-oriented |
| Starts at the deal level | Starts with roll-ups and drills down to deals |

## Combined interview answer

> At Aviso, Deals and Forecasting are closely connected.
>
> The Deals module helps users understand and act on individual sales opportunities. It provides information such as deal stage, amount, close date, activity, engagement, risk signals, and recommended actions.
>
> The Forecasting module aggregates those opportunities across representatives, managers, regions, and the overall organization to estimate expected revenue. It allows leaders to compare submitted forecasts with AI predictions and drill down to the individual deals responsible for forecast changes.
>
> I contributed to frontend workflows, configurable tables, filtering, drill-down experiences, analytics visualizations, API integration, performance optimization, and production issue resolution across these modules.

## Easiest way to remember the distinction

> **Deals explains the health of each opportunity. Forecasting explains the expected revenue produced by the complete set of opportunities.**

---

# Final Preparation Checklist

Before using these answers in an interview, replace generic statements with verified details from your work:

- Which screens or components did you personally own?
- Which APIs did you integrate or develop?
- What data volume did the module handle?
- What was the exact performance problem?
- How did you measure the improvement?
- Which production incident did you resolve?
- Which identifiers were used in the real integration?
- Were webhooks, polling, queues, or scheduled jobs actually used?
- Was the health score rule-based, model-based, or both?
- Which parts belonged to another team?

When you did not own an implementation, say:

> I did not directly own that part, but my understanding of the system flow is...
