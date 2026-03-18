# Deploy Runbook (Starter)

This folder is a scaffold. A typical production deployment:
- containerize each service
- put an ingress (nginx, ALB, or cloud gateway) in front
- run Postgres + Redis as managed services

## Minimum production checklist
- Set `WEB_SECRET_KEY` to a strong secret
- Configure Stripe signing secret for webhooks
- Replace in-memory stores with Postgres-backed models
- Turn on structured logging and centralize logs
- Add backups for Postgres and run migrations safely

