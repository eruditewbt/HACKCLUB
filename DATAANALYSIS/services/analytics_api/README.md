# analytics_api

SaaS-ready API for the **Data Health Monitor** vertical slice.

## Run

```bash
cd C:\Users\eruditewbt\Documents\GitHub\HACKCLUB\DATAANALYSIS
pip install -r requirements.txt
uvicorn services.analytics_api.app:app --reload --port 8000
```

## Multi-Tenancy

All endpoints that return org-specific data require:

- Header: `X-Org-ID: your-org`

## Endpoints

- `GET /health`

- `POST /run`
  - Multipart: `csv` (required), `rules` (optional JSON)
  - Form: `dataset_name`, optional `webhook_url`, optional `max_rows`
  - Returns `run_id`, `report_url`, and score metadata

- `GET /report/{run_id}`
  - DB-backed when `DATABASE_URL` is set

- `GET /runs`
  - Requires Postgres (`DATABASE_URL`)

- `GET /drift/{dataset_name}`
  - Requires >=2 stored runs for that dataset

## Storage

Set `DATABASE_URL` to enable Postgres storage for:
- runs
- profiles
- validations
- HTML reports

