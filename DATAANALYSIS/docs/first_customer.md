# First Customer Scenario (MVP)

Target user: a small data team that runs weekly/monthly reports and keeps getting surprised by broken CSV exports or schema changes.

## Offer
"Send us your dataset and data contract. We run a daily data health check and alert you when something breaks."

## What they get
- A premium HTML report they can forward to stakeholders
- A quality score trend (once Postgres is enabled)
- Alerts to their ops channel via webhook

## API Demo (curl)

1) Run a report:

```bash
curl -X POST http://localhost:8000/run \
  -H "X-Org-ID: demo" \
  -F "dataset_name=sales" \
  -F "csv=@datasets/samples/sales.csv" \
  -F "rules=@datasets/samples/sales.rules.json"
```

2) Open the report:

```text
http://localhost:8000/report/{run_id}
```

## Webhook Payload
When validation fails, we send:

```json
{
  "event": "data_validation_failed",
  "org_id": "...",
  "dataset_name": "...",
  "run_id": "...",
  "failed_checks": 12,
  "total_checks": 900,
  "quality_score": 0.986
}
```
