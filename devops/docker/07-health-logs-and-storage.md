# 7. Health, Logs, and Files

## Health check

A health check asks: **Is the app working?**

- `/health`: Is FastAPI running?
- `/ready`: Is FastAPI ready to receive requests?

Docker, a load balancer, or a hosting service can call these routes.

## Restart after failure

```yaml
restart: unless-stopped
```

Docker restarts the container if it crashes or the laptop/server restarts.

## Logs

Your app should print logs normally. Docker collects them.

```bash
docker compose logs -f backend
```

Do not print passwords or tokens in logs.

Limit log size:

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

## Files inside a container

Containers can be deleted and recreated. Files saved only inside them may be lost.

Keep important data in:

- MongoDB Atlas or another database
- S3 or Cloudinary
- A Docker volume when local server storage is enough

For your production apps, prefer a managed database and cloud file storage.

