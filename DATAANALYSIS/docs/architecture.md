# Architecture (DATAANALYSIS)

This repo is structured like a deployable product.

## Library Layers
- `io/`: dataset ingestion adapters (CSV now; DB/connectors next)
- `profiling/`: schema inference + column statistics
- `quality/`: contract rules + validators
- `viz/`: HTML report generation
- `pipelines/`: orchestration that writes artifacts per run

## Deployable Layers
- `services/analytics_api/`: FastAPI service exposing profiling/validation/report endpoints.

## Artifacts
Each run produces:
- `artifacts/{run_id}.json`: full profile + validation results
- `artifacts/{run_id}.html`: human-readable report (when validation runs)
- `artifacts/latest.json`: pointer to the latest run

## Next (Production)
- Persist artifacts to Postgres + object storage
- Add connectors (Postgres/MySQL, Google Sheets, Stripe, Shopify)
- Add governance (catalog, lineage, audit)
- Add multi-tenant boundary (org_id) + RBAC
