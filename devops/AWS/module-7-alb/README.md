# Module 7 — Add the Application Load Balancer

## Goal

Reach production using the AWS-provided ALB hostname.

```text
Browser -> ALB :80 -> Target group -> Prod EC2 :80 -> Nginx -> FastAPI
```

## Lessons

1. [Create security groups and target group](1.security-and-target-group.md)
2. [Create and test the ALB](2.create-and-test-alb.md)
3. [Add a domain and HTTPS later](3.https-later.md)

One EC2 target is enough for learning, but it is not highly available.
