# WEB

Production-grade, monetizable Python web ecosystem that covers:
- FastAPI (core APIs + an API gateway)
- Flask (microapps: landing pages + webhook receiver)
- Django (full SaaS dashboard/admin)
- Shared platform modules (auth, billing, observability, security, contracts)
- Infra (docker/compose/nginx/CI templates)

This is structured like a real platform repo, not a tutorial dump.

## Folder Layout

```
.
├── web_platform/
│   ├── shared/
│   ├── fastapi/
│   ├── flask/
│   └── django/
├── infra/
├── docs/
└── examples/
```

Why `web_platform/` exists: keeping code under a real package avoids name collisions with `fastapi`, `flask`, and `django` dependencies.

## Quick Start (Local)

### 1) Start Postgres + Redis

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

### 2) Run FastAPI Gateway (recommended entrypoint)

```bash
pip install -r web_platform/fastapi/api_gateway/requirements.txt
python -m uvicorn web_platform.fastapi.api_gateway.main:app --reload --port 8000
```

Health: `GET http://localhost:8000/health`

### 3) Run Flask Webhooks

```bash
pip install -r web_platform/flask/webhooks/requirements.txt
python web_platform/flask/webhooks/app.py
```

### 4) Run Django SaaS Admin

```bash
pip install -r web_platform/django/saas_app/requirements.txt
python web_platform/django/saas_app/manage.py migrate
python web_platform/django/saas_app/manage.py runserver 8001
```

## Environment Variables

Copy `.env.example` and set values for your environment.

Important variables:
- `WEB_SECRET_KEY`: used for JWT signing (demo). Use a strong secret in prod.
- `WEB_DATABASE_URL`: points to Postgres (demo uses sqlite in Django until wired).
- `WEB_REDIS_URL`: for rate limiting, sessions, queues (scaffold).

## Monetization Primitives Included

- Plans and entitlements scaffold (`shared/billing/plans.py`)
- API gateway hooks for API keys + rate limiting (`fastapi/api_gateway/main.py`)
- Usage events endpoint scaffold (`POST /v1/usage/events`)
- Webhook verification + idempotency scaffold (Stripe-style signature)

## What To Build Next (Production Checklist)

- Replace in-memory stores with Postgres models
- Implement API key issuance + hashing + revocation in Django admin
- Add background jobs (Celery/RQ) for webhook processing and emails
- Add real billing providers (Stripe/Paystack) and subscription state machine
- Add observability: metrics + tracing + dashboards
- Add tests: unit + integration + contract tests (OpenAPI)

## Docs
- Architecture: `docs/architecture/overview.md`
- Runbooks: `docs/runbooks/`

## Examples
- Curl scripts: `examples/curl/`
