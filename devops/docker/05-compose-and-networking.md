# 5. Run Frontend and Backend Together

Docker Compose starts multiple containers using one file.

Create `compose.yaml`:

```yaml
services:
  backend:
    build: ./backend
    env_file: .env
    expose:
      - "8000"
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Run everything:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up -d
```

Stop everything:

```bash
docker compose down
```

## How do containers talk?

Compose gives each container a name.

The frontend reaches FastAPI using:

```text
http://backend:8000
```

Here, `backend` is the service name in `compose.yaml`.

Only frontend port `80` is open to users. Backend port `8000` stays inside Docker.

