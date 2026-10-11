# Module 1: AWS essentials for a complete beginner

## Goal

This module builds the mental model needed to deploy FastAPI. It does not create AWS resources yet, so you can study it without incurring charges.

By the end, you will understand this flow:

```text
User
  -> Domain name
  -> AWS load balancer
  -> EC2 server
  -> Nginx
  -> FastAPI
  -> MongoDB Atlas and S3
```

## Lessons

Read these files in order:

1. [Cloud, Regions, and Availability Zones](1.cloud-regions-and-availability-zones.md)
2. [IAM identities, roles, and permissions](2.iam-and-permissions.md)
3. [VPC networking and security groups](3.vpc-networking.md)
4. [EC2 servers and EBS disks](4.ec2-and-ebs.md)
5. [Docker, ECR, Nginx, and FastAPI](5.application-runtime.md)
6. [Load balancer, domain, and HTTPS](6.alb-route53-and-https.md)
7. [S3, MongoDB Atlas, and configuration](7.data-files-and-configuration.md)
8. [Monitoring and server access](8.cloudwatch-and-session-manager.md)
9. [Complete architecture and revision](9.complete-architecture.md)

## How to study

For each lesson:

1. Read the explanation.
2. Draw the diagram yourself.
3. Answer the questions without looking at the answers.
4. Continue only when the main idea is clear.

You do not need to memorize AWS console screens. You need to understand what each component does and why it exists.

## Vocabulary used throughout

| Word | Simple meaning |
|---|---|
| Cloud | Renting computing resources over the internet |
| Resource | Something created in AWS, such as a server or bucket |
| Service | An AWS product, such as EC2 or S3 |
| Instance | One running virtual server |
| Deploy | Put an application on a server so users can access it |
| Request | A message sent by a client to an API |
| Response | The result returned by the API |
| Port | A numbered network entry point, such as `80` or `443` |
| Inbound | Traffic entering a resource |
| Outbound | Traffic leaving a resource |
| Environment | An isolated setup such as development or production |

## The one rule to remember

Every AWS component in this course must have a clear purpose. If you cannot explain why a resource is needed, do not create it yet.
