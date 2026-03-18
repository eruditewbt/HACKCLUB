# DATAANALYSIS (Data Health Monitor)

A production-shaped, monetizable **data reliability** toolkit:

- Profile datasets
- Enforce data contracts (validation rules)
- Produce premium HTML reports (Executive Summary + Issues + Recommendations)
- Persist run history to Postgres (multi-tenant by `org_id`)
- Send operational alerts via webhook
- Detect drift across historical runs

This is designed to become a sellable product:
> "Upload your data -> get a professional data quality report + alerts + history"

## Quickstart

### 1) Install

```bash
cd C:\Users\eruditewbt\Documents\GitHub\HACKCLUB\DATAANALYSIS
pip install -r requirements.txt
```

### 2) Configure (recommended)

Copy `.env.example` into your environment and set:
- `DATABASE_URL` (Postgres)
- `DA_WEBHOOK_URL_DEFAULT` (optional)

### 3) CLI (one command)

```bash
python -m dataanalysis_platform run-all \
  --input datasets/samples/sales.csv \
  --rules datasets/samples/sales.rules.json \
  --org-id demo \
  --dataset sales
```

Output:
- `artifacts/{run_id}.json`
- `artifacts/{run_id}.html`
- Stored in Postgres when `DATABASE_URL` is set

### 4) API (FastAPI)

```bash
uvicorn services.analytics_api.app:app --reload --port 8000
```

Health:
- `GET /health`

Run pipeline:
- `POST /run`
  - Header: `X-Org-ID: <org>`
  - Form-data: `csv` (file), optional `rules` (json file)
  - Form: `dataset_name`, optional `webhook_url`, optional `max_rows`

Reports:
- `GET /report/{run_id}` (requires `X-Org-ID`)

History:
- `GET /runs?dataset_name=...` (requires Postgres + `X-Org-ID`)

Drift:
- `GET /drift/{dataset_name}` (needs >=2 stored runs)

## Repo Layout

- `dataanalysis_platform/`: reusable library code
- `services/analytics_api/`: API you can deploy
- `datasets/samples/`: sample datasets + rule specs
- `docs/`: architecture notes
- `DICT/`: existing NLP assets (kept as-is for future semantic layer work)

## Sellable MVP Scope

- Persist every run (who/what/when) in Postgres
- Multi-tenant by `X-Org-ID`
- Webhook alerts on failures
- Premium report output that feels like a consultant delivered it

