# Module 7: Background, scheduled, and bulk-sync jobs

FastAPI handles HTTP requests. It does not provide a durable job scheduler by itself. This module explains where job code belongs and how to choose between an in-process task, a separate scheduled worker, and a one-off sync script.

## Outcomes

You will be able to:

- distinguish immediate, scheduled, periodic, and one-off jobs;
- explain why important jobs should not live only inside a web process;
- schedule an email for a specific UTC time using a database-backed job;
- run a separate worker that safely claims and executes due jobs;
- split a large Zendesk/CRM sync by tenant and API page;
- checkpoint progress, retry safely, and use idempotent bulk upserts;
- run jobs independently from the FastAPI server.

## Lessons

1. [Choose the correct job type](1.job-types.md)
2. [Scheduled email design](2.scheduled-email-design.md)
3. [Scheduled email implementation](3.scheduled-email-implementation.md)
4. [Bulk CRM sync design](4.bulk-sync-design.md)
5. [Bulk CRM sync implementation](5.bulk-sync-implementation.md)
6. [Running and operating jobs](6.running-jobs.md)

## Main rule

If losing a job would affect a user or business process, store the job durably before returning success. A coroutine kept only in process memory disappears when that process restarts.
