# Deploying FastAPI on AWS: Simple Learning Plan

## Goal

Deploy one FastAPI application in two separate environments:

- **Development:** one small EC2 instance.
- **Production:** one dedicated EC2 instance behind an Application Load Balancer.
- **Web server:** Nginx in front of FastAPI on both instances.
- **Database:** MongoDB hosted in Atlas.
- **Public endpoint:** the AWS-provided ALB DNS name over HTTP for now.

We will not use Auto Scaling yet. It will be easier to learn after the single-server production deployment is working.

## Final architecture

### Development

```text
Developer
   |
   v
Dev EC2 public address
   |
   v
Nginx :80
   |
   v
FastAPI :8000
   |
   v
MongoDB Atlas
```

### Production

```text
Users
  |
  v
Application Load Balancer :80
  |
  v
Target Group + /health check
  |
  v
Production EC2
  |
  v
Nginx :80 -> FastAPI :8000
                       |
                       v
                 MongoDB Atlas
```

The production load balancer initially has one EC2 target. It gives us a stable endpoint and health checks. We can add a domain, HTTPS, and Auto Scaling later.

## Environment separation

| Resource | Development | Production |
|---|---|---|
| Compute | Dev EC2 | Prod EC2 |
| Load balancer | Not required | Application Load Balancer |
| MongoDB Atlas | Development database | Production database |
| Configuration | `/fastapi/dev/...` | `/fastapi/prod/...` |
| Address | EC2 public IP | AWS-provided ALB DNS name |

Development and production must not share credentials or databases.

## Modules

### Module 1 — AWS essentials and architecture

[Open Module 1 lessons](module-1-aws-essentials/README.md)

Learn only what this deployment uses:

- AWS Regions and Availability Zones
- IAM users, roles, and policies
- EC2 and EBS
- VPC, subnet, route table, internet gateway, and security group
- ECR
- Application Load Balancer and target groups
- Route 53 and ACM
- Parameter Store and CloudWatch
- How a request reaches FastAPI

**Outcome:** You can explain every component in the architecture.

### Module 2 — Prepare FastAPI for deployment

[Open Module 2 lessons](module-2-prepare-fastapi/README.md)

- Add `/health` and `/ready` endpoints
- Read configuration from environment variables
- Configure MongoDB Atlas without hard-coded credentials
- Add graceful startup and shutdown
- Create a production Dockerfile
- Run FastAPI with Uvicorn
- Keep application instances stateless

**Outcome:** One container image can run in dev or prod using different configuration.

### Module 3 — Account safety and cost controls

[Open Module 3 lessons](module-3-account-safety-and-cost/README.md)

- Enable MFA on the root account
- Create an administrator identity for normal work
- Configure an AWS Budget and billing alerts
- Select one AWS Region
- Use an EC2 IAM role instead of access keys
- Understand the costs of EC2, ALB, storage, and data transfer

**Outcome:** The AWS account has basic security and billing protection.

### Module 4 — Explore S3 (optional)

[Open Module 4 lessons](module-4-s3-deferred/README.md)

Learn the basic concepts and optionally create a test bucket. Application integration remains postponed.

### Module 5 — Deploy the development environment

[Open Module 5 lessons](module-5-deploy-development/README.md)

- Launch one small Ubuntu EC2 instance
- Configure its security group
- Connect with AWS Systems Manager Session Manager where possible
- Install Docker and Nginx
- Push the application image to Amazon ECR
- Pull and run the FastAPI container
- Configure Nginx as a reverse proxy to port `8000`
- Store dev settings in SSM Parameter Store
- Connect to the Atlas development database
- Test `/health`, `/ready`, `/docs`, and MongoDB

**Outcome:** The development API runs through Nginx on one EC2 instance.

### Module 6 — Deploy the production EC2 instance

[Open Module 6 lessons](module-6-deploy-production/README.md)

- Launch a separate production EC2 instance
- Attach the application IAM role
- Install Docker and Nginx
- Pull the approved image from ECR
- Use production parameters and credentials
- Configure the container to restart automatically
- Configure a minimal production Nginx reverse proxy
- Connect only to the Atlas production database
- Verify the application before exposing it publicly

**Outcome:** Production runs independently from development.

### Module 7 — Add the Application Load Balancer

[Open Module 7 lessons](module-7-alb/README.md)

- Create an internet-facing Application Load Balancer
- Create a target group containing the production EC2 instance
- Configure `/health` as the target health check
- Allow EC2 web traffic only from the load balancer security group
- Understand listeners, target groups, and healthy targets
- Use the AWS-provided ALB DNS name over HTTP
- Add a domain, ACM, and HTTPS later

**Outcome:** The AWS-provided ALB URL reaches the production FastAPI server.

### Module 8 — Logging, deployment, and maintenance

[Open Module 8 lessons](module-8-operations/README.md)

- View application and Nginx logs
- Send important logs to CloudWatch
- Add simple alarms for unhealthy targets, high CPU, and HTTP 5xx errors
- Build and push a new Docker image
- Update dev first, verify it, and then update prod
- Plan GitHub Actions after the manual deployment is understood
- Back up important configuration
- Patch and restart the server safely
- Remove unused AWS resources to avoid unexpected charges

**Outcome:** You can operate and update the application without guessing.

## Deployment order

```text
Prepare FastAPI
    -> Secure AWS account
    -> Create ECR repository
    -> Deploy dev EC2 + Nginx
    -> Deploy prod EC2 + Nginx
    -> Connect MongoDB Atlas
    -> Add ALB
    -> Add logs and basic deployment automation
```

## What each module will contain

1. Only the concepts required for that module
2. A small architecture explanation
3. Exact AWS Console steps
4. Required commands and configuration files
5. Verification steps
6. Common mistakes
7. Cleanup instructions for billable resources

## What we are skipping for now

- Auto Scaling Groups
- Launch Templates and instance refreshes
- Kubernetes and EKS
- ECS and Fargate
- Lambda
- Terraform and CloudFormation
- Multi-region deployment
- Complex CI/CD pipelines
- Blue/green and canary deployments
- Self-hosted MongoDB
- Advanced multi-account networking

## Important decisions

### Why keep the load balancer with only one production instance?

It provides:

- one stable public endpoint;
- target health checks;
- a clean path to add more instances later.

For a very small personal application, the ALB can be skipped to reduce cost. We include it because learning load balancing is one of the goals.

### Why use Nginx behind the load balancer?

The ALB handles public routing and health checks. Nginx provides a stable local reverse proxy to FastAPI, access logs, request-size limits, and timeout configuration. Its configuration will remain minimal.

### Why use IAM roles?

The EC2 instances receive temporary AWS credentials automatically. We do not store permanent AWS access keys in source code, environment files, or server disks.

## Completion checklist

The initial course is complete when:

- dev and prod run on separate EC2 instances;
- each environment uses separate settings and Atlas databases;
- Docker starts FastAPI automatically;
- Nginx proxies requests to FastAPI;
- the ALB health check passes;
- production is available through the ALB URL;
- secrets are not committed to Git;
- basic logs and alarms are available;
- a new version can be tested in dev and then deployed to prod;
- all billable resources can be identified and removed.

## Later: Auto Scaling

After this course, Auto Scaling can be added as a separate module:

```text
Launch Template
    -> Auto Scaling Group
    -> Attach existing ALB target group
    -> Minimum/desired/maximum capacity
    -> Scaling policy
    -> Instance replacement and deployment refresh
```

The existing Docker image, Nginx configuration, health endpoint, ALB, and Atlas database can all be reused.

## Primary references

- [AWS: Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html)
- [AWS: ALB target groups and health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html)
- [MongoDB Atlas: AWS networking](https://www.mongodb.com/docs/atlas/manage-vpc-peering/)
