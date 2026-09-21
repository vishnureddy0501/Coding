1. Tell me about yourself
    “Hi, I’m Vishnu Vardhan Reddy. I’m a full-stack software engineer with over three years of experience, currently working at Aviso AI.
    My primary expertise is in frontend development using Vue.js and React.js, and I also work on backend services using Node.js, Express.js, FastAPI, MongoDB, and Redis.
    
    At Aviso AI, I have contributed to products such as Sales Engagement, Customer Success Intelligence, notifications, real-time chat, deals, and forecasting. My work includes developing end-to-end features, building dashboards and data visualizations, integrating APIs, improving application performance, and resolving production issues.
    
    I have also worked on architectural improvements such as microfrontends, migrating Vue 2 applications to Vue 3, introducing lazy loading and code splitting, and removing RxJS to simplify the codebase. Recently, I have also led a team of three engineers, performed code reviews, and mentored team members.

    I enjoy solving product and engineering problems that require both good user experience and reliable backend design. I’m now looking for an opportunity where I can take greater ownership and contribute to scalable, high-impact products.”

2. Walk me through your résumé
“I completed my B.Tech in Computer Science from JNTUK, graduating with an 8.5 CGPA and ranking among the top students in my department.
During college, I strengthened my problem-solving skills by solving more than a thousand competitive-programming problems. I also completed internships at CDAC and Backflipt Software. At CDAC, I worked on interactive network and teletraffic visualizations using Vue.js and D3.js. At Backflipt, I worked on a no-code application-building platform, where I resolved UI issues, developed organizational visualizations, and implemented authentication using JWT, Gmail OAuth, and email verification.
In October 2023, I joined Aviso AI as an Associate Software Engineer. I initially worked on modules such as deals, forecasts, activity intelligence, and relationship intelligence. I contributed to the Vue 2-to-Vue 3 migration, microfrontend development, analytics visualizations, and performance optimization.
I later moved into a Software Engineer role with greater ownership. I have worked on Sales Engagement, Customer Success Intelligence, notifications, and real-time chat. Along with developing features, I resolve production issues, review code, mentor engineers, and coordinate with product, design, QA, and backend teams.”

3. How to explain any project
Use this order:
1. What problem did the project solve?
2. Who used it?
3. What did you personally own?
4. How did the system work?
5. What technical challenge did you face?
6. How did you solve it?
7. What was the result?
8. What would you improve now?
A compact project answer should follow:
Problem → Responsibilities → Technical approach → Challenge → Result

Avoid beginning with a list of technologies. Explain the product first and the technology afterward.
4. Sales Engagement Platform
Tell me about the project
“One of my major projects was a Sales Engagement Platform designed to help sales representatives manage and automate prospect outreach.
The platform allowed users to manage prospects, create email sequences, generate email content using AI, schedule emails, track activities, and monitor prospect engagement from one place.
I worked across the frontend and backend. On the frontend, I used Vue.js and Vuex to build prospect-management screens, campaign workflows, scheduling interfaces, and a rich-text email editor using Quill.js. I integrated Gmail APIs to support email composition, sending, receiving, scheduling, and template management.
On the backend, I worked with Express.js and MongoDB to build REST APIs for prospects, activities, email tracking, and campaign workflows. I also handled data synchronization between the UI, backend services, and email provider.
A major challenge was maintaining consistent state across prospect updates, scheduled actions, and email activity. We addressed this by defining clear workflow states, validating transitions on the backend, and refreshing affected frontend data after important operations.
The resulting platform reduced repetitive manual work and helped users manage their outreach more efficiently.”
What was your exact contribution?
“I owned features across the complete development lifecycle. I clarified requirements with product and design teams, developed frontend components, integrated APIs, implemented backend changes where required, tested edge cases, participated in code reviews, and supported the features after production deployment.
My main contributions included prospect management, the Quill.js email editor, Gmail integration, email scheduling, activity tracking, templates, and responsive UI development.”
Why did you use Quill.js?
“We needed a rich-text editor that supported formatted email composition and could be customized for our product requirements. Quill.js provided a structured document model, formatting support, event handling, and extensibility.
I integrated it with our email workflow, handled content changes, validated empty or invalid content, and ensured that the generated HTML was suitable for email delivery. One challenge was that content rendered by a browser editor may appear differently in email clients, so the produced markup needed to remain simple and compatible.”
How did email scheduling work?
“When a user scheduled an email, the frontend collected the content, recipients, schedule time, and relevant prospect or campaign information. The backend validated the request and stored the scheduling details.
A background process or scheduling service then identified emails that were ready to be sent and used the Gmail integration to send them. After the send attempt, the system updated the email status and activity history so that the frontend could display whether the email was scheduled, sent, or failed.
We also had to consider time-zone handling, duplicate execution, invalid authentication tokens, and failures from the email provider.”
How did you measure the impact?
“We evaluated the impact through product-usage data and business metrics such as the time users spent managing outreach, the number of manual steps eliminated, campaign activity, and response rates. Based on the internal measurements available to the team, productivity improved by approximately 30%, and campaign response rates improved by around 25%.”
Only use this answer if you know where those measurements came from.
5. Customer Success Intelligence
Tell me about this project
“Customer Success Intelligence is a platform that helps Customer Success Managers understand the condition of customer accounts from a unified dashboard.
Previously, relevant information such as account details, support tickets, product usage, engagement, and business metrics could be spread across different systems. The platform consolidated that information and presented health indicators, recent activity, and trends in one place.
I contributed to account-management screens, ticket tracking, search and filtering, configurable views, dashboards, API integration, role-based access, and performance improvements. I worked with Vue.js and React.js on the frontend and Express.js, FastAPI, and MongoDB-backed services on the backend.
One of the main challenges was combining data from multiple sources while keeping the dashboard responsive and accurate. We reduced unnecessary requests, loaded independent information in parallel, added appropriate loading and error states, and avoided rerendering expensive visualizations unnecessarily.
This allowed Customer Success Managers to identify risks and engagement changes more quickly and take proactive action.”
How did you combine data from multiple sources?
“We treated the backend as an aggregation layer instead of requiring the frontend to understand every external source.
The services fetched information from the required systems, transformed it into a consistent internal format, and exposed it through APIs designed around frontend use cases. On the client side, we requested independent datasets in parallel where possible and displayed partial results without blocking the complete page.
We also handled missing data, stale data, service failures, and inconsistent identifiers explicitly so that one unavailable source would not necessarily break the entire dashboard.”
How did you implement RBAC?
“We separated authentication from authorization. Authentication identified the current user, while authorization determined what that user could access.
The backend validated the user’s identity and permissions before returning protected data or allowing an action. The frontend used the permission information to show or hide relevant controls, but we never treated frontend checks as the security boundary.
This ensured that users could access only the accounts, views, and actions allowed by their role.”
How did you optimize the dashboard?
“I first looked for the actual bottleneck using browser performance tools, network timings, and component-level observation.
Depending on the feature, our improvements included parallelizing independent requests, avoiding duplicate API calls, lazy-loading noncritical components, paginating or virtualizing large datasets, debouncing search, caching stable data, and memoizing expensive calculations.
For charts, I avoided recreating the entire chart when only the dataset changed. I also made loading states more granular so that one slow widget did not block the entire dashboard.”
6. Real-Time Chat Application
Explain your chat application
“I worked on a real-time chat application that supported messaging, online presence, conversation management, and file sharing.
React was used for the frontend, while Node.js, Express.js, and MongoDB supported the backend. REST APIs handled operations such as authentication, retrieving conversations, and loading message history. WebSockets handled events that needed immediate delivery, such as new messages and user presence.
When a user sent a message, the server authenticated the connection, validated the conversation membership, persisted the message, and emitted the event to connected participants. The clients then updated their local state.
For media sharing, files were stored in Amazon S3 rather than in the application server or database. The database stored only the required metadata and file reference.
The main challenges were maintaining message consistency, handling reconnections, preventing unauthorized access to conversations, and keeping the UI synchronized across multiple clients.”
Why use both REST APIs and WebSockets?
“REST is suitable for request-response operations such as login, fetching conversation history, creating a conversation, or loading user details.
WebSockets are suitable for server-initiated, low-latency events such as new messages, typing indicators, and online-status changes.
Using both kept the architecture simple: REST handled normal resource operations, while WebSockets handled real-time updates.”
How did you avoid losing messages?
“The database was treated as the source of truth. A message was validated and persisted before, or as part of, broadcasting the successful event.
The client used temporary state to provide immediate feedback, but it reconciled that state with the confirmed server response. After a reconnection, the client could request messages after its last known message or timestamp.
For a larger production system, I would also consider idempotency keys, delivery acknowledgements, retry policies, ordering identifiers, and a message broker for horizontal scaling.”
Why store files in S3?
“Storing large files directly in the application database or serving them from application instances would increase database load and make scaling more difficult.
S3 provides durable object storage and works well with CDNs and controlled access. The application stores file metadata and object references in the database, while the actual content is stored in S3.
For private files, I would use restricted buckets and short-lived presigned URLs instead of exposing files publicly.”
7. Vue 2 to Vue 3 Migration
Explain the migration
“One of my important engineering contributions was helping migrate an existing application from Vue 2 to Vue 3.
The application was already in production, so we could not rewrite everything at once. We first identified incompatible dependencies and reusable patterns, then migrated the application incrementally.
My work included updating components and lifecycle behavior, replacing deprecated APIs, resolving dependency incompatibilities, testing existing workflows, and coordinating changes across shared modules.
The main challenge was preserving existing behavior while changing the framework underneath it. We reduced the risk by migrating in smaller units, reviewing changes carefully, and validating critical workflows through regression testing.”
Why was the migration necessary?
“Vue 3 provided better long-term maintainability, improved performance, modern APIs, better TypeScript support, and continued ecosystem support. Remaining on Vue 2 would have increased technical debt and made it harder to adopt actively maintained dependencies.”
8. Why did you remove RxJS?
“RxJS was being used in areas where the same behavior could be implemented using simpler framework-native state management and event patterns.
Although RxJS is powerful for complex asynchronous streams, it introduced an additional mental model and made some parts of the application harder to understand and debug.
We identified each observable flow, understood its behavior, replaced it incrementally, and verified that subscriptions, cleanup, error handling, and state updates continued to work correctly. This reduced complexity and made the application easier for the broader team to maintain.”
Do not suggest that RxJS is inherently bad. Explain that it was unnecessary for your application’s use cases.
9. Microfrontends
What are microfrontends?
“Microfrontends apply the idea of independently manageable services to frontend applications. Instead of maintaining the complete frontend as one tightly coupled application, it is divided into business-oriented modules that can be developed and maintained with clearer ownership.
At Aviso AI, this helped us organize major product modules more independently and improve modularity. Shared concerns such as authentication, navigation, design systems, and communication still had to be standardized.
The main benefits were separation of concerns and team ownership. The trade-offs included dependency duplication, inconsistent UI, integration complexity, and communication between modules.”
How did modules communicate?
“Communication depended on the relationship between the modules. Shared global information could be provided through a controlled common layer, while loosely coupled modules could communicate through events or agreed interfaces.
We tried to avoid one microfrontend directly depending on another module’s internal implementation. Clear contracts were important so that one module could change without unexpectedly breaking another.”
10. Leadership questions
Tell me about leading three engineers
“In my current role, I have led a team of three engineers for feature delivery. My responsibility was not just assigning tasks; I helped clarify requirements, divided work based on dependencies, reviewed technical approaches, performed code reviews, and supported engineers when they were blocked.
I also coordinated with product, QA, design, and backend stakeholders to ensure everyone understood the expected behavior and delivery timeline.
I tried to keep ownership with each engineer rather than controlling every implementation detail. At the same time, I monitored integration points and quality so that separately developed pieces worked correctly together.”
How do you conduct code reviews?
    “I review code for correctness first, followed by edge cases, readability, performance, security, testing, and consistency with the existing architecture.
    I try to explain why I am suggesting a change instead of simply asking for a rewrite. I distinguish required corrections from optional improvements and avoid blocking a pull request over personal style preferences when the project’s conventions are already satisfied.”
How do you mentor junior developers?
“I first try to understand whether the person is blocked by missing technical knowledge, unclear requirements, or unfamiliarity with the codebase.
Instead of immediately providing the final solution, I explain how to break down the problem, where to inspect the existing flow, and how to validate possible solutions. After implementation, I use code reviews to reinforce reusable principles.”
11. Production and debugging questions
Tell me about a production issue you resolved
“One type of production issue I handled involved an edge case that worked for common data but failed for certain customer configurations.
I first gathered the exact reproduction steps, affected users, logs, API responses, and recent code changes. I then reproduced the problem in a controlled environment and traced the data from the UI through the API and database.
After identifying the incorrect assumption, I implemented a narrow fix, added validation for the edge case, and tested related workflows to avoid regression. We released the fix through the normal deployment process and monitored the affected flow afterward.
The main lesson was that production bugs often appear because real customer data contains combinations that are not covered by normal test cases.”
Replace this with a real incident before an interview.
How do you debug a slow page?
“I divide the problem into network time, JavaScript execution, rendering, and backend processing.
I use the browser’s network panel to identify slow or duplicate requests and performance tools to find expensive renders or long-running tasks. I check whether large bundles, repeated state updates, expensive components, or excessive DOM elements are involved.
If the API is slow, I inspect server timings, database queries, external-service calls, payload size, and caching opportunities. I optimize only after identifying the actual bottleneck and compare measurements before and after the change.”
12. Behavioral questions
What is your biggest strength?
“My main strength is end-to-end ownership. I can understand a product requirement, develop the frontend experience, work with backend APIs and data, handle edge cases, and support the feature after deployment. This helps me identify integration problems early instead of treating frontend and backend work as completely separate responsibilities.”
What is your weakness?
“Earlier, I sometimes spent too much time trying to perfect an implementation before sharing it. I learned that early feedback is more valuable, especially when requirements may change. I now discuss the proposed approach early, deliver in smaller increments, and separate essential improvements from optional refinements.”
Why are you looking for a change?
“I have learned a great deal in my current role, especially about full-stack product development, production ownership, performance, and team leadership. I’m now looking for broader technical ownership and an environment where I can work on challenging systems at a larger scale while continuing to grow as an engineer.”
Avoid criticizing your current company.
Why should we hire you?
“You should consider me because I combine strong frontend experience with practical backend and production ownership. I have worked on complex business products involving dashboards, real-time communication, email integration, microfrontends, authentication, and data visualization.
I can contribute at multiple stages—from requirement analysis and system design to implementation, debugging, code review, and production support. I also have experience guiding other engineers and collaborating across teams.”
Tell me about a failure
“In one situation, I underestimated the complexity of a feature because I focused primarily on the normal workflow and did not identify all external dependencies early enough. During implementation, additional edge cases affected the original estimate.
I communicated the risk, divided the remaining work into critical and optional parts, and worked with the team to deliver the essential functionality safely. Since then, I explicitly identify dependencies, failure scenarios, migration requirements, and test cases before committing to an estimate.”
Use a genuine example and explain what changed in your behavior.
How do you handle disagreements?
“I first make sure we agree on the actual goal and constraints. Then I compare the options using evidence such as maintainability, performance, implementation cost, user impact, and existing project conventions.
If both approaches are reasonable, I prefer a small proof of concept or measurement rather than a prolonged opinion-based discussion. Once the team makes a decision, I support it even if my original suggestion was different.”
13. Common rapid-fire questions

What is your current role?
    “I’m a Software Engineer at Aviso AI. I develop end-to-end product features, improve performance, resolve production issues, review code, and lead a team of three engineers.”
What is your strongest technology?
    “My strongest area is frontend engineering with Vue.js and React.js. I’m also comfortable developing backend APIs with Node.js, Express.js, and MongoDB.”
What kind of applications have you built?
    “I have worked on sales-engagement systems, customer-success platforms, analytics dashboards, forecasting and deal-management modules, notification systems, real-time chat, organizational visualizations, and network analytics.”
What are you looking for?
“I’m looking for a product-engineering role where I can own meaningful features, solve scaling and performance problems, and contribute to both technical decisions and team delivery.”
14. Questions you must prepare from real experience
Write down specific answers to these before interviewing:
- How many users or customers used each project?
- What was the approximate volume of prospects, emails, messages, or dashboard records?
- What was the slowest page or API before optimization?
- What was its performance after optimization?
- How were the 30% and 25% improvements calculated?
- What exact feature did you personally design?
- What was the most difficult production bug you resolved?
- What design decision did you disagree with?
- What did you implement in FastAPI?
- Where and why was Redis used?
- How were microfrontends deployed and integrated?
- How did authentication and token refresh work?
- How were scheduled emails executed?
- How did email tracking work?
- How were WebSocket connections authenticated?
- How did chat work across multiple server instances?
- What tests did you write?
- How was the application deployed?
- What did you monitor in production?
If you cannot answer one of these, do not invent an answer. Say:
“I did not directly own that part, but my understanding of the flow is…”

That sentence is much safer and more credible than pretending to own the entire system.
Final preparation method
For each major project, prepare four versions:
- One sentence: what the product does.
- Thirty seconds: problem, users, and your role.
- Two minutes: architecture, contribution, challenge, and impact.
- Deep dive: APIs, database design, security, performance, failures, testing, deployment, and trade-offs.
Your goal is not to memorize paragraphs. Memorize these five anchors for every project:
Problem → My ownership → Architecture → Hardest challenge → Measurable result