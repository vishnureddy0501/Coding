# Docker: Simple Production Guide

We will use this example:

```text
User
  |
  v
Nginx
  |-- /      -> React frontend
  |-- /api   -> FastAPI backend
                    |
                    v
               MongoDB Atlas
```

Nginx is the front door. The backend and database stay behind it.

## Learn in this order

1. [Basic ideas](01-docker-fundamentals.md)
2. [Commands](02-essential-commands.md)
3. [Backend](03-production-backend.md)
4. [Frontend](04-production-frontend.md)
5. [Run everything together](05-compose-and-networking.md)
6. [Settings and passwords](06-configuration-and-secrets.md)
7. [Health, logs, and files](07-health-logs-and-storage.md)
8. [Security](08-security-and-optimization.md)
9. [Deploy and update](09-deployment-and-updates.md)
10. [Final checklist](10-production-checklist.md)

Do not learn Kubernetes now. Docker and Docker Compose are enough.

