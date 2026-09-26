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

Product usage tells a Customer Success Manager whether a customer is actively using the product.

We mainly track:

- Number of active users
- Number of logins
- Important features used
- Number of actions completed
- Last activity date
- Whether usage is increasing or decreasing

## How is it tracked?

When a user performs an important action, the frontend or backend records an event.

For example, when a user submits a forecast:

```json
{
  "accountId": "account_245",
  "userId": "user_891",
  "eventName": "forecast_submitted",
  "timestamp": "2026-09-21T08:30:00Z"
}
```

The `accountId` tells us which customer performed the action. The `userId` tells us which user performed it.

## Simple flow

```text
User performs an action
        ↓
Application records the event
        ↓
Backend stores and processes usage events
        ↓
Events are grouped by customer account
        ↓
Daily or weekly metrics are calculated
        ↓
Customer Success dashboard displays the metrics
```

For example, the backend can calculate this account summary:

```json
{
  "accountId": "account_245",
  "weeklyActiveUsers": 84,
  "totalLogins": 310,
  "forecastsSubmitted": 46,
  "usageTrend": "decreasing",
  "lastActivityAt": "2026-09-21T08:30:00Z"
}
```

The frontend receives this summarized data and displays it using KPIs, tables, and charts. It does not process all raw events in the browser.

## Why is this useful?

A Customer Success Manager can use these metrics to identify:

- Customers who are actively using the product
- Customers who are not adopting important features
- Accounts whose usage is decreasing
- Customers who may require training or support
- Accounts that may be at risk of churn

## Interview answer

> We tracked important user actions such as logins, feature usage, and completed workflows. Each action was recorded with the account, user, action name, and timestamp.
>
> The backend grouped these events by customer account and calculated daily or weekly metrics such as active users, login count, feature adoption, last activity, and usage trend. The Customer Success dashboard displayed the summarized metrics through KPIs and charts. These metrics also helped Customer Success Managers identify low-adoption or at-risk accounts and could be used as inputs to the account health score.

---

# 3. Account Health Scoring

## Definition

An account health score is a number between 0 and 100 that represents the overall condition of a customer account.

It helps a Customer Success Manager quickly identify:

- Healthy customers
- Customers who need attention
- Customers who may be at risk

## Main inputs

Use four simple categories. Give each category its own score between 0 and 100.

| Category | What it measures |
|---|---|
| Product usage | Active users, important features used, and usage trend |
| Support | Open tickets, critical tickets, and unresolved-ticket age |
| Engagement | Meetings, emails, responses, and recent customer activity |
| Sentiment | Survey results, customer feedback, or CSM assessment |

## Simple calculation

For a simple example, give every category equal importance:

```text
Health score =
    Product usage score × 25%
  + Support score       × 25%
  + Engagement score    × 25%
  + Sentiment score     × 25%
```

Example:

```text
Product usage = 80
Support       = 60
Engagement    = 70
Sentiment     = 90

Health score = (80 + 60 + 70 + 90) / 4
             = 75
```

The account's health score is `75/100`.

## Health status

| Score | Status | Meaning |
|---:|---|---|
| 75–100 | Green | Healthy |
| 50–74 | Amber | Needs attention |
| 0–49 | Red | At risk |

These categories, weights, and ranges are examples. A real customer may configure different weights. For example, one customer may give product usage 40% importance and support only 20%.

If one category has no data, do not automatically give it zero. Mark it as unavailable or calculate the score using only the available categories.

## Simple flow

```text
Collect product, support, engagement and sentiment data
                         ↓
Calculate a score for each category
                         ↓
Apply configured weights
                         ↓
Calculate final score from 0 to 100
                         ↓
Display Green, Amber or Red status
```

## Interview answer

> The account health score is a value between 0 and 100 that shows the overall condition of a customer account. We calculate separate scores for product usage, support, engagement, and customer sentiment.
>
> We combine those category scores using configured weights and map the final value to Green, Amber, or Red. The dashboard also shows the individual category scores so the CSM can understand why an account is healthy or at risk and decide what action to take.

---

# 4. Support-Ticket Synchronization

Support tickets may originate in systems such as Zendesk, Jira Service Management etc.

### Short version

> We collect product-usage metrics, combine them with support, engagement, and sentiment scores to calculate account health, and synchronize support tickets from external systems. This gives Customer Success Managers one place to understand customer activity and risk.

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
