# Deploy this FastAPI app to one AWS EC2 instance

This is the smallest useful AWS deployment:

```text
Browser / Postman
       |
       v
EC2 public IP:8000
       |
       v
Docker container running this FastAPI app
```

There is only **one EC2 instance**. No load balancer, custom VPC work, auto scaling, domain, HTTPS, or CI/CD in this guide.

## Before starting

1. Push this `Coding` repository to GitHub if it is not already there.
2. Ensure the app works on your laptop:

   ```bash
   cd devops/docker/fastapi-app
   docker compose up --build -d
   curl http://localhost:8000/health
   ```

## 1. Create the EC2 instance

In AWS Console, open **EC2** → **Instances** → **Launch instances**.

Use these values:

| Field | Value |
|---|---|
| Name | `fastapi-demo` |
| AMI | Ubuntu Server 24.04 LTS |
| Instance type | `t3.micro` |
| Key pair | Create/select one, then download the `.pem` file safely |
| Network settings | Keep the default VPC and default subnet selected |
| Auto-assign public IP | Enable |
| Storage | Keep the default |

In **Network settings**, add these inbound rules:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | My IP |
| Custom TCP | 8000 | Anywhere (`0.0.0.0/0`) |

Click **Launch instance**. Wait until its state is `Running`, then copy its **Public IPv4 address**.

## 2. Connect to the instance

On your laptop, run this from the directory containing your downloaded key:

```bash
chmod 400 YOUR_KEY.pem
ssh -i YOUR_KEY.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

You are now inside the EC2 machine.

## 3. Install Docker and Git

Run these commands on EC2:

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
exit
```

The final `exit` is important. Connect again so your user can run Docker without `sudo`:

```bash
ssh -i YOUR_KEY.pem ubuntu@YOUR_EC2_PUBLIC_IP
docker --version
docker compose version
```

## 4. Download this project onto EC2

On EC2, replace the URL with your repository URL:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL coding
cd coding/devops/docker/fastapi-app
```

If the repository is private, use its SSH clone URL after configuring GitHub SSH access on EC2, or clone with a GitHub fine-grained access token.

## 5. Create the environment file

The `.env` file is not copied from your laptop or Git. Create it directly on EC2:

```bash
nano .env
```

Paste this basic configuration:

```env
APP_NAME=FastAPI AWS Demo
APP_ENV=production
DEBUG=false
WELCOME_MESSAGE=Hello from AWS EC2
DEMO_SECRET=replace-this-with-any-value
```

Save with `Ctrl + O`, press `Enter`, then exit with `Ctrl + X`.

## 6. Start the application

Still inside `devops/docker/fastapi-app`, run:

```bash
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

The health command should return a successful response.

## 7. Open it from your laptop

Replace `YOUR_EC2_PUBLIC_IP` with the address copied in step 1:

```text
http://YOUR_EC2_PUBLIC_IP:8000/
http://YOUR_EC2_PUBLIC_IP:8000/docs
http://YOUR_EC2_PUBLIC_IP:8000/health
```

Use `/docs` to test the API in Swagger UI.

## Deploy a later code change

Push your change from your laptop. Then SSH into EC2 and run:

```bash
cd ~/coding/devops/docker/fastapi-app
git pull
docker compose up --build -d
curl http://localhost:8000/health
```

That rebuilds the Docker image and replaces the running container with the latest code.

## Stop or start the app

Run these on EC2 from the project folder:

```bash
# Stop containers
docker compose down

# Start them again
docker compose up -d
```

## What you have after this guide

```text
One EC2 instance
  └── Docker Compose
       └── One FastAPI container on port 8000
```

This is suitable for learning and a basic demo. If the EC2 instance stops, the app is unavailable until that instance is available again.
