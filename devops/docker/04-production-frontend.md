# 4. Docker for React

React production code is only HTML, CSS, and JavaScript.

Node.js builds it. Nginx shows it to users.

```dockerfile
# Build React
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Serve React
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

This uses two steps:

```text
Node.js builds React -> Nginx serves the built files
```

Node.js is not kept in the final image. This makes the image smaller.

## Simple Nginx configuration

```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass http://backend:8000;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }
}
```

- `/api` goes to FastAPI.
- Everything else goes to React.
- `try_files` makes React Router work after page refresh.

