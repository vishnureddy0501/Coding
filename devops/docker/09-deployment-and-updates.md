# 9. Deploy and Update

## First deployment

```text
1. Test code
2. Build image
3. Give image a version
4. Upload image to Docker Hub or AWS ECR
5. Server downloads image
6. Server starts containers
7. Check health and logs
```

## Update the application

```bash
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail=100 backend
```

Docker downloads the new image and replaces the old container.

## Rollback

Rollback means returning to the previous working version.

Example:

```text
New version: my-api:1.0.1  -> has a problem
Old version: my-api:1.0.0  -> works correctly
```

Change the image version back to `1.0.0` and run:

```bash
docker compose up -d
```

## One-server limitation

Updating one server may cause a few seconds of downtime. That is acceptable for a small project.

Later, multiple servers and a load balancer can avoid downtime.

