from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from automation.engine.retries import RetryPolicy


@dataclass(frozen=True)
class TaskSpec:
    id: str
    type: str
    inputs: Dict[str, Any]
    depends_on: List[str]
    retry: RetryPolicy
    idempotency_key: Optional[str] = None


@dataclass(frozen=True)
class WorkflowSpec:
    workflow_id: str
    tasks: List[TaskSpec]


def _parse_retry(obj: Dict[str, Any]) -> RetryPolicy:
    r = obj or {}
    return RetryPolicy(
        max_attempts=int(r.get("max_attempts", 1)),
        base_delay_s=float(r.get("base_delay_s", 0.5)),
        max_delay_s=float(r.get("max_delay_s", 10.0)),
    )


def load_workflow(path: str) -> WorkflowSpec:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    wf_id = str(data.get("workflow_id") or "workflow")
    tasks: List[TaskSpec] = []
    for t in data.get("tasks", []):
        tasks.append(
            TaskSpec(
                id=str(t["id"]),
                type=str(t["type"]),
                inputs=dict(t.get("inputs") or {}),
                depends_on=[str(x) for x in (t.get("depends_on") or [])],
                retry=_parse_retry(t.get("retry") or {}),
                idempotency_key=(t.get("idempotency_key") or None),
            )
        )

    return WorkflowSpec(workflow_id=wf_id, tasks=tasks)
