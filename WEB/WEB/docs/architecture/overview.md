# Architecture Overview

This repository is structured like a real platform:
- FastAPI: API-first services and gateway
- Django: dashboard/admin UX and operational tooling
- Flask: lightweight microapps (marketing + webhooks)
- Shared: security/auth/billing/observability contracts

## Core domain (monetization-ready)
- `Org`: customer account / workspace
- `Subscription`: plan + entitlement source of truth
- `ApiKey`: paid API access primitive
- `UsageEvent`: metering input for billing/quotas
- `AuditLog`: operational traceability

## Service boundary guidance
- Gateway is the public edge (rate limiting, API keys, auth token checks)
- Auth service issues tokens and manages identities (demo store in this scaffold)
- Billing service consumes webhooks (idempotent) and updates subscription state
- Analytics service ingests events and produces aggregates

