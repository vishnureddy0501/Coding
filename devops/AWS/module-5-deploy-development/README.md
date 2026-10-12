# Module 5 — Deploy development

## Goal

Run the development FastAPI container on one EC2 instance through Nginx.

```text
Your browser -> Dev EC2 :80 -> Nginx -> Docker :8000 -> FastAPI -> Atlas dev DB
```

## Lessons

1. [Create ECR and push the image](1.ecr-and-image.md)
2. [Create the dev EC2 role and parameter](2.role-and-parameter.md)
3. [Launch the dev EC2 instance](3.launch-ec2.md)
4. [Install, run, and verify](4.run-and-verify.md)

## Result

```text
http://<dev-ec2-public-ip>/docs
```
