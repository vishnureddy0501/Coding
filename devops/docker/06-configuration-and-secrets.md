# 6. Settings and Passwords

Examples of settings:

- Development or production mode
- Database URL
- Secret key
- API key

## Local development

Keep them in `.env`:

```env
APP_ENV=development
MONGODB_URL=mongodb+srv://replace-me
JWT_SECRET=replace-me
```

Load the file in Compose:

```yaml
env_file: .env
```

Add `.env` to both `.gitignore` and `.dockerignore`.

## Production

Store secrets in your hosting platform or AWS Parameter Store. Pass them when the container starts.

```text
Same image + dev settings  = dev app
Same image + prod settings = prod app
```

Never keep passwords in:

- Code
- Dockerfile
- Docker image
- GitHub
- React environment variables

Users can see values included in React code. Private keys belong only in the backend.

