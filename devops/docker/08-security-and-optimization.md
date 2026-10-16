# 8. Simple Security Rules

Follow these rules:

1. Never add `.env` to an image or GitHub.
2. Run the backend as a normal user, not root.
3. Open only the Nginx port to users.
4. Keep the database private.
5. Use separate passwords for dev and prod.
6. Update and rebuild images regularly.
7. Use small official images such as `python:3.12-slim`.

## Use version names

Do not depend only on `latest`.

```text
my-api:1.0.0
my-api:1.0.1
```

If `1.0.1` has a problem, you can quickly return to `1.0.0`.

## HTTPS

Docker does not create HTTPS.

HTTPS is normally handled by:

- AWS Load Balancer
- Your hosting platform
- Nginx with a certificate

Start with the option provided by your hosting platform.

