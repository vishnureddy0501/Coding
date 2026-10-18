# FastAPI: Local, Dev and Production

This project supports three separate environments:

```text
Your feature branch
       |
       v
1. Local laptop -----> develop branch -----> 2. Dev EC2
                                                   |
                                              QA/frontend test
                                                   |
                                                   v
                         main branch/tag -----> 3. Production EC2
```

Do not run dev and production from the same container or `.env` file.

## Project structure

```text
fastapi-app/
├── app/
│   ├── config.py       # Reads environment variables
│   └── main.py         # FastAPI application
├── .env                # Local values; never commit
├── .env.example        # Safe example; commit this
├── compose.yaml
├── Dockerfile
└── requirements.txt
```

## Environment summary

| Environment | Runs where? | Code source | Configuration | Used by |
|---|---|---|---|---|
| Local | Your laptop | Feature branch | Local `.env` | Developer |
| Dev | Dev EC2 | `develop` branch | Dev values/secrets | Developer, QA and frontend |
| Production | Prod EC2 | Approved `main` tag | Production values/secrets | Real users |

Use separate dev and production EC2 instances. Their data, secrets and URLs must also be separate.

# 1. Fast local development

For daily coding, run Python directly with auto-reload. You do not need to rebuild Docker after every code change.

## First-time setup

```bash
cd devops/docker/fastapi-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with local values:

```env
APP_NAME=FastAPI Local
APP_ENV=development
DEBUG=true
WELCOME_MESSAGE=Hello from local
DEMO_SECRET=local-demo-value
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Whenever you save a Python file, Uvicorn automatically restarts the application.

Open:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## Test the Docker image before pushing

Do this after your feature is working locally:

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f
```

Stop it with:

```bash
docker compose down
```

## Local secrets

- Keep local values in `.env` for fast development.
- `.env` is ignored by Git and is not copied into the Docker image.
- Never put permanent AWS access keys in `.env`.
- Use your AWS profile only when you intentionally need to test AWS Parameter Store locally.

# 2. Deploy changes to the shared dev instance

The dev instance is the shared testing environment for QA and frontend developers.

```text
Frontend/QA ---> dev URL ---> Dev EC2 ---> Dev Docker container
```

## One-time dev EC2 setup

1. Create a dedicated Ubuntu EC2 instance.
2. Install Git, Docker and Docker Compose.
3. Clone the repository.
4. Check out the `develop` branch.
5. Create a dev `.env` file on that EC2 instance.
6. Allow the required API port in its Security Group.

Install the tools:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Log out and reconnect after adding your user to the Docker group.

Example dev configuration:

```env
APP_NAME=FastAPI Dev
APP_ENV=dev
DEBUG=false
WELCOME_MESSAGE=Hello from the shared dev server
DEMO_SECRET=dev-secret-placeholder
```

## Deploy each change to dev

First, test locally and push your changes:

```bash
git checkout develop
git merge YOUR_FEATURE_BRANCH
git push origin develop
```

Then connect to the dev EC2 instance and run:

```bash
cd YOUR_REPOSITORY_PATH/devops/docker/fastapi-app
git checkout develop
git pull origin develop
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

QA and frontend can now use:

```text
http://DEV_EC2_IP:8000
http://DEV_EC2_IP:8000/docs
```

Check errors with:

```bash
docker compose logs -f
```

Once this manual flow is clear, CI/CD can run the same deployment commands automatically whenever `develop` is updated.

# 3. Deploy approved changes to production

Production uses a separate EC2 instance and production configuration.

Only deploy after:

1. The feature works locally.
2. The Docker image works locally.
3. QA approves it on the dev instance.
4. The code is reviewed and merged into `main`.

## Create a release

```bash
git checkout main
git merge develop
git tag v1.0.0
git push origin main --tags
```

The tag gives the deployed code a fixed version. Use a new version such as `v1.0.1` for the next release.

## Deploy the release on production EC2

```bash
cd YOUR_REPOSITORY_PATH/devops/docker/fastapi-app
git fetch --tags
git checkout v1.0.0
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

Example production configuration:

```env
APP_NAME=FastAPI Production
APP_ENV=production
DEBUG=false
WELCOME_MESSAGE=Hello from production
DEMO_SECRET=production-secret-placeholder
```

Do not expose the FastAPI port directly in a real production system. Put Nginx or an Application Load Balancer in front and use HTTPS.

## Roll back if the release fails

Checkout the previous working tag and rebuild:

```bash
git checkout PREVIOUS_WORKING_TAG
docker compose up --build -d
curl http://localhost:8000/health
```

# Secrets in dev and production

The simple practice app reads all values from environment variables. A real AWS application should use:

```text
Non-sensitive values ---> runtime environment variables
Sensitive values ------> AWS Parameter Store SecureString
AWS permission --------> IAM role attached to EC2
```

Use separate Parameter Store paths:

```text
/fastapi-demo/dev/database-url
/fastapi-demo/prod/database-url
```

The EC2 IAM role reads the correct path. Do not copy AWS access keys into `.env` or the Docker image.

# Complete release flow

```text
1. Create feature branch
2. Develop quickly with local .env and --reload
3. Test the Docker image locally
4. Merge into develop
5. Deploy develop to Dev EC2
6. QA and frontend test it
7. Merge approved code into main and create a version tag
8. Deploy that exact tag to Production EC2
9. Run the health check and inspect logs
```

For learning, manual deployments are fine. The next improvement is CI/CD that builds one Docker image and promotes that same image from dev to production.

## AWS cost note

Two running EC2 instances can cost money. Stop the dev instance when nobody is testing. A public IP may change after stopping the instance; use an Elastic IP or DNS when you need a stable dev URL.
