# FastAPI services
Core API services and a simple gateway.

Services:
- `api_gateway`: public entrypoint (API keys, rate limiting hooks, request IDs)
- `auth_service`: signup/login/refresh (demo persistence)
- `billing_service`: plans + stripe webhook verification scaffold
- `analytics_service`: usage event ingestion scaffold

