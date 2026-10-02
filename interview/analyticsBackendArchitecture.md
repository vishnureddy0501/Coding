# How Our Analytics Data Reaches the Dashboard

## 1. Sending the event

The frontend sends this event when a user visits the account details page:

```js
this.recordEvent({
    eventName: "AccountPage|Details",
    data: {
        routeName: this.$route.name,
        accountId: this.$route.params.accountId,
        AccountName: this.getAccountDetails.account_info.account_name
    }
});
```

`recordEvent()` is usually a wrapper around the third-party analytics SDK or API. It may also add information such as:

- User or tenant ID
- Session ID
- Event time
- Application and environment

The third-party analytics platform stores this event.

## 2. How grouping works

The event name follows this naming convention:

```text
AccountPage|Details
     |         |
   group     action
```

- `AccountPage` represents the page or feature group.
- `Details` represents the action or section inside that group.

The event name can be separated like this:

```js
const [group, action] = eventName.split("|");
```

The resulting values are:

```text
group  = AccountPage
action = Details
```

The analytics provider can then show all `AccountPage` events together and show `Details` as an action inside that group.

The `|` character does not have a universal meaning in every analytics product. The grouping must be implemented in one of these places:

- Inside your `recordEvent()` wrapper
- In the third-party analytics configuration
- In the query used to read analytics data
- In your backend while importing the data

To find the exact place, check the implementation of `recordEvent()` and the event payload visible in the analytics platform.

## 3. Complete data flow

```text
Vue application
    ↓ sends events
Third-party analytics platform
    ↓ stores events
Scheduled job runs every 12 hours
    ↓ fetches events through the provider's API
Our backend processes and saves the data
    ↓
Our frontend requests the data from our backend
    ↓
Analytics dashboard displays it
```

Your dashboard is not reading each event immediately. It displays the most recently imported data, so it may be up to 12 hours behind.

## 4. The 12-hour sync job

This is called a **scheduled batch job**, **periodic sync job**, or **cron job**.

The cron expression for running a job every 12 hours is:

```text
0 */12 * * *
```

Each time the job runs, it should:

1. Read the time of the last successful sync.
2. Request newer events from the third-party analytics API.
3. Fetch every page if the API uses pagination.
4. Separate `AccountPage|Details` into its group and action if necessary.
5. Group the events by tenant, account, event and date.
6. Insert new summaries or update existing summaries in the database.
7. Save the new successful-sync time.

For example, multiple raw events can become one summary:

```text
accountId: 123
group: AccountPage
action: Details
date: 2026-10-01
eventCount: 48
uniqueUsers: 12
lastUsedAt: 2026-10-01T18:30:00Z
```

The dashboard calls your backend API, and the backend reads this prepared summary from your database.

## 5. What to use in Express.js

For a small application, a library such as `node-cron` can start the sync every 12 hours:

```js
cron.schedule("0 */12 * * *", syncAnalytics);
```

For a production application, prefer one of these:

- A queue worker using BullMQ and Redis
- A Kubernetes CronJob
- A cloud scheduler that triggers a separate worker

Running a cron job directly inside every Express server instance can cause the same job to run multiple times when the application has multiple replicas. It can also miss a run when the server restarts.

## 6. What to use in FastAPI

For a small application, APScheduler can schedule the sync.

For a production application, prefer one of these:

- Celery Beat schedules the job, and a Celery worker runs it.
- A Kubernetes CronJob runs a separate sync process.
- A cloud scheduler triggers a worker or protected endpoint.

The FastAPI request server should not perform a long analytics import inside a normal user request.

## 7. Avoiding duplicate data

The job may retry after a failure, so saving the same analytics data again must not create duplicates.

Use a unique identity such as:

```text
tenantId + accountId + eventName + date
```

Use an **upsert**:

- Insert the summary if it does not exist.
- Update it if it already exists.

Also use a job lock so that two workers cannot run the same sync at the same time.

## Interview answer

> Our Vue application sends events such as `AccountPage|Details` to a third-party analytics provider. We use the first part as the feature group and the second part as the action. A scheduled batch job runs every 12 hours, fetches events created after the last successful sync, aggregates them by tenant, account and event, and upserts the summaries into our database. The dashboard reads these summaries through our backend API. In production, I would run this using a dedicated queue worker, Kubernetes CronJob or cloud scheduler rather than an in-process cron inside every API server.
