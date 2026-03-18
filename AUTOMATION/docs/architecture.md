# Architecture

- automation/engine: execution
- automation/packs: integrations
- workflows: templates

Phase 2:
- scheduler: `automation/engine/scheduler.py` (cron/interval, file-based schedules)
- triggers: `automation/engine/triggers.py` (poll-based filesystem trigger)
- API: `services/automation_api/app.py` (optional FastAPI wrapper)
