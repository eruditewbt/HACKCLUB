# AUTOMATION (Automation OS)

A production-shaped, monetizable **automation platform** for running workflows end-to-end with minimal human intervention.

## What You Get (MVP)

- Workflow engine (tasks + dependencies + retries)
- Artifacts per run (logs, outputs)
- File-based state store (idempotency + run history)
- CLI to run workflows and inspect results
- Two sellable packs:
  - Data Health pack (bridges to your `DATAANALYSIS/` project)
  - Web Monitor pack (HTTP checks + alert hooks)

## Quickstart

```bash
cd AUTOMATION
python -m automation run --workflow workflows/templates/hello_world.json --org-id demo
```

Artifacts are written to `artifacts/<run_id>/`.

## Configure

See `.env.example`.

## Workflow Format

Workflows are JSON:
- `workflow_id`
- `tasks[]` with: `id`, `type`, optional `depends_on`, `inputs`, optional `retry`, optional `idempotency_key`
