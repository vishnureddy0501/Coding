# 10. Production Checklist

## Image

- [ ] `.dockerignore` exists.
- [ ] `.env` is not inside the image.
- [ ] Backend runs as a normal user.
- [ ] Image has a version such as `1.0.0`.

## Network

- [ ] Only Nginx is public.
- [ ] Backend stays inside the Docker network.
- [ ] Database is not open to everyone.
- [ ] HTTPS is enabled by the hosting platform or load balancer.

## Application

- [ ] `/health` and `/ready` work.
- [ ] Containers restart after failure.
- [ ] Logs do not contain passwords.
- [ ] Log size is limited.
- [ ] Important files are not stored only inside containers.

## Deployment

- [ ] Tests pass before deployment.
- [ ] Dev and prod have separate settings.
- [ ] Health and logs are checked after deployment.
- [ ] The previous image version is available for rollback.

That is enough for your first production Docker setup.

