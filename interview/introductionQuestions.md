# Introduction and Common Interview Questions

Use these answers as speaking points. Do not memorize every word. Keep your delivery natural and replace generic examples with facts from your experience.

## Contents

1. [Tell me about yourself](#1-tell-me-about-yourself)
2. [Walk me through your résumé](#2-walk-me-through-your-résumé)
3. [Explaining a project](#3-explaining-a-project)
4. [Leadership questions](#4-leadership-questions)
5. [Production and debugging](#5-production-and-debugging)
6. [Behavioral questions](#6-behavioral-questions)
7. [Rapid-fire questions](#7-rapid-fire-questions)
8. [Questions to ask the interviewer](#8-questions-to-ask-the-interviewer)
9. [Final preparation](#9-final-preparation)

---

# 1. Tell Me About Yourself

## 60–90 second answer

> Hi, I'm Vishnu Vardhan Reddy. I'm a full-stack software engineer with over three years of experience, currently working at Aviso AI.
>
> My strongest area is frontend development using Vue.js and React.js. I also work with Node.js, Express.js, FastAPI, MongoDB, and Redis on the backend.
>
> At Aviso, I have contributed to Sales Engagement, Customer Success Intelligence, Deals, Forecasting, notifications, and real-time chat. My work includes building end-to-end features, dashboards, data visualizations, API integrations, performance improvements, and resolving production issues.
>
> I have also worked on microfrontends, a Vue 2-to-Vue 3 migration, lazy loading, code splitting, and simplifying the codebase by removing unnecessary RxJS usage. I currently lead three engineers, review code, and mentor team members.
>
> I'm looking for an opportunity where I can take greater ownership and contribute to scalable, high-impact products.

## 30-second answer

> I'm a full-stack software engineer with over three years of experience, currently working at Aviso AI. I primarily work with Vue.js and React.js, along with Node.js, Express.js, FastAPI, MongoDB, and Redis. I have built features for sales engagement, customer success, deals, forecasting, analytics, and real-time chat. I also have experience with performance optimization, microfrontends, production debugging, and leading a small team.

## Structure to remember

```text
Current role
    ↓
Main technical skills
    ↓
Important products and responsibilities
    ↓
Leadership or special contribution
    ↓
What you want next
```

---

# 2. Walk Me Through Your Résumé

> I completed my B.Tech in Computer Science from JNTUK with an 8.5 CGPA. During college, I developed strong problem-solving skills through competitive programming and solved more than a thousand problems.
>
> I completed internships at CDAC and Backflipt Software. At CDAC, I worked on network and teletraffic visualizations using Vue.js and D3.js. At Backflipt, I worked on a no-code application platform, organizational visualizations, and authentication using JWT, Gmail OAuth, and email verification.
>
> In October 2023, I joined Aviso AI as an Associate Software Engineer. I initially contributed to Deals, Forecasting, Activity Intelligence, and Relationship Intelligence. I also worked on microfrontends, analytics visualizations, performance improvements, and the Vue 2-to-Vue 3 migration.
>
> I later moved into a Software Engineer role with greater ownership. I have worked on Sales Engagement, Customer Success Intelligence, notifications, and real-time chat. Along with feature development, I resolve production issues, review code, mentor engineers, and coordinate with product, design, QA, and backend teams.

## Important difference

- **Tell me about yourself:** Focus on who you are now and your strongest experience.
- **Walk me through your résumé:** Explain your career chronologically.

---

# 3. Explaining a Project

Use this order:

```text
Problem
   ↓
Users
   ↓
My contribution
   ↓
Technical approach
   ↓
Main challenge and solution
   ↓
Result
```

## Project-answer template

> The project was built to solve **[business problem]** for **[type of user]**.
>
> My responsibility was **[your actual contribution]**. I worked mainly with **[important technologies]**.
>
> At a high level, the system worked by **[simple technical flow]**.
>
> The main challenge was **[specific challenge]**. We solved it by **[solution]**.
>
> The result was **[measurable or observable outcome]**.

Do not start by listing technologies. Explain the product and business problem first.

## Prepare three versions

- **One sentence:** What the product does
- **One minute:** Problem, users, contribution, and result
- **Deep dive:** Architecture, APIs, data, failures, security, and trade-offs

Detailed project notes are available in:

- [project.md](./project.md)
- [salesEngagement.md](./salesEngagement.md)
- [productUsageTracking.md](./productUsageTracking.md)
- [supportTicketSync.md](./supportTicketSync.md)

---

# 4. Leadership Questions

## Tell me about leading three engineers

> I led three engineers during feature delivery. I helped clarify requirements, divided work based on dependencies, reviewed technical approaches, conducted code reviews, and supported engineers when they were blocked.
>
> I also coordinated with product, design, QA, and backend teams. I gave each engineer ownership of their work while monitoring integration points, timelines, and quality.

## How do you conduct code reviews?

> I first check correctness and edge cases, followed by readability, performance, security, tests, and consistency with the existing architecture.
>
> I explain why I am suggesting a change and distinguish required corrections from optional improvements. I avoid blocking a pull request over personal style preferences when project conventions are already satisfied.

## How do you mentor junior developers?

> I first identify whether the person is blocked by unclear requirements, missing technical knowledge, or unfamiliarity with the codebase.
>
> Instead of immediately giving the final solution, I help them break down the problem, identify the relevant code flow, and validate possible solutions. I then use code reviews to reinforce reusable principles.

---

# 5. Production and Debugging

## Tell me about a production issue you resolved

> I handled a production issue that worked for normal data but failed for a particular customer configuration.
>
> I collected reproduction steps, logs, API responses, affected data, and recent code changes. I reproduced the issue in a controlled environment and traced the data from the UI through the API and database.
>
> After finding the incorrect assumption, I implemented a focused fix, tested related workflows for regression, deployed it through the normal process, and monitored the result.
>
> The main lesson was to include real customer-data variations and edge cases during design and testing.

Replace this with a real incident before using it in an interview.

Detailed notes: [performance.md](./performance.md)

---

# 6. Behavioral Questions

## What is your biggest strength?

> My main strength is end-to-end ownership. I can understand a requirement, build the frontend experience, work with backend APIs and data, handle edge cases, and support the feature after deployment. This helps me identify integration problems early.

## What is your weakness?

> One weakness I've been working on is that I sometimes spend more time than necessary trying to find the most optimal solution, especially when I'm working on a technical problem.

Earlier, I would keep exploring different approaches even after finding a solution that was already good enough for the requirements. With experience, I've become better at balancing technical quality with delivery timelines.

Now, I first understand the requirements and constraints, implement a clean and maintainable solution, and then evaluate whether further optimization actually provides meaningful value. This has helped me make decisions faster without compromising code quality.


## Why are you looking for a change?

> I have learned a great deal in my current role, especially about full-stack product development, production ownership, performance, and team leadership. I'm now looking for broader technical ownership and an opportunity to work on challenging systems at a larger scale.

Do not criticize your current company, manager, or team.

## Why should we hire you?

> I combine strong frontend experience with practical backend and production ownership. I have worked on dashboards, real-time communication, email integration, microfrontends, authentication, and data visualization.
>
> I can contribute from requirement analysis and implementation through debugging, code review, and production support. I also have experience guiding engineers and collaborating with cross-functional teams.

## Tell me about a failure

> I once underestimated a feature because I focused on the normal flow and did not identify every dependency early enough. Additional edge cases affected the original estimate.
>
> I communicated the risk, divided the remaining work into essential and optional parts, and worked with the team to deliver the critical functionality safely.
>
> Since then, I identify dependencies, failure cases, migration requirements, and testing needs before committing to an estimate.

Use a genuine example. The important part is what changed in your behavior.
---

# 7. Rapid-Fire Questions

## What is your current role?

> I'm a Software Engineer at Aviso AI. I develop end-to-end product features, improve performance, resolve production issues, review code, and lead three engineers.

## What is your strongest technology?

> My strongest area is frontend engineering with Vue.js and React.js. I'm also comfortable developing backend APIs using Node.js, Express.js, FastAPI, and MongoDB.

## What kinds of applications have you built?

> I have worked on sales-engagement systems, customer-success platforms, analytics dashboards, forecasting and deal-management modules, notifications, real-time chat, organizational visualizations, and network analytics.

## What are you looking for?

> I'm looking for a product-engineering role where I can own meaningful features, solve performance and scaling problems, and contribute to technical decisions and team delivery.

---

# 8. Questions to Ask the Interviewer

When the interviewer asks, “Do you have any questions for me?”, ask two or three thoughtful questions. Do not say “No” unless the interviewer has already answered everything.

## Best general questions

These work in most technical or hiring-manager rounds:

1. **What would you expect the person in this role to accomplish during the first three to six months?**
2. **What are the most important technical or product challenges the team is currently solving?**
3. **How does the team make architecture and technical decisions?**
4. **How is success measured for this role?**
5. **What does the development process look like from requirement to production?**

You usually need only two or three.

## Questions for a technical interviewer

- What is the current frontend and backend architecture?
- What performance or scalability challenges does the system currently have?
- How does the team handle testing, code reviews, deployment, and production monitoring?
- How much ownership do engineers have over design and implementation decisions?
- Is there any major migration or technical-debt project planned?

## Strong closing question

> Based on our conversation, is there any area of my experience that you would like me to clarify further?

This gives you an opportunity to address a concern before the interview ends.

## Example selection for a technical round

> Yes, I have a couple of questions. What are the main technical challenges the team is currently working on? Also, what would you expect the person joining this role to accomplish in the first three to six months?

## What not to ask

Avoid questions that:

- Can be answered easily from the company website
- Focus only on leave, salary, or promotions during the first technical round
- Suggest that you did not read the job description
- Ask for confidential information
- Were already answered during the interview
- Have a negative assumption, such as “Why do people leave this team?”

## The best approach

Listen during the interview and ask a follow-up question based on the conversation:

> You mentioned that the team is migrating part of the application. What is the main reason for the migration, and what role would this position play in it?

A relevant follow-up question is usually stronger than a memorized generic question.

---

# 9. Final Preparation

## Facts you must know from your experience

- Your exact contribution to each project
- Approximate users, records, messages, or requests handled
- One meaningful production issue
- One performance improvement with before-and-after measurements
- One difficult technical decision
- How authentication and authorization worked
- How important background jobs were executed
- Which parts you owned and which belonged to other teams
- How claimed percentage improvements were measured

If you did not directly own something, say:

> I did not directly own that component, but my understanding of the flow is...

Do not invent implementation details.

## Final project formula

For every project, remember these five points:

```text
Problem
   ↓
My ownership
   ↓
Architecture
   ↓
Hardest challenge
   ↓
Result
```
