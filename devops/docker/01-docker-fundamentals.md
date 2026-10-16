# 1. Docker Basics

## Why use Docker?

Your app needs Python, Node.js, packages, and settings.

Docker packs them in one standard package. The same package can run on your laptop and server.

## Dockerfile

A file containing steps to pack the app.

Think of it as a recipe.

## Image

The packed app created from a Dockerfile.

Think of it as a class or template. It is not running yet.

## Container

A running copy of an image.

```text
Dockerfile -> Image -> Container
   recipe     package    running app
```

One image can start many containers.

## Registry

An online place that stores images.

Examples: Docker Hub and AWS ECR.

```text
Laptop uploads image -> Registry -> Server downloads image
```

## Port

A port is like a door number.

The container runs on your laptop, but it has its own small network.

```bash
docker run -p 8080:8000 my-api
```

```text
laptop port 8080 -> container port 8000 -> FastAPI
```

Read it as:

```text
laptop port : container port
     8080   :      8000
```

You open `localhost:8080`. Docker forwards it to FastAPI listening on port `8000` inside the container.

## Remember

- Image = packed app.
- Container = running app.
- Registry = place that stores images.
- Dockerfile = instructions to create an image.
