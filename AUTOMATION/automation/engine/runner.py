from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List

from automation.engine.artifacts import RunArtifacts
from automation.engine.context import RunContext
from automation.engine.observability import EventLogger
from automation.engine.retries import run_with_retries
from automation.engine.state_store import FileStateStore
from automation.engine.workflow import WorkflowSpec


@dataclass
class RunSummary:
    run_id: str
    org_id: str
    workflow_id: str
    ok: bool
    tasks: Dict[str, Any]


def _toposort(tasks: List[Dict[str, Any]]) -> List[str]:
    deps = {t["id"]: set(t.get("depends_on") or []) for t in tasks}
    out: List[str] = []
    ready = [tid for tid, ds in deps.items() if not ds]

    while ready:
        tid = ready.pop(0)
        out.append(tid)
        for k, ds in deps.items():
            if tid in ds:
                ds.remove(tid)
                if not ds and k not in out and k not in ready:
                    ready.append(k)

    if len(out) != len(deps):
        missing = set(deps.keys()) - set(out)
        raise ValueError(f"Workflow has cycles or missing deps; unresolved: {sorted(missing)}")

    return out


class WorkflowRunner:
    def __init__(self, *, registry):
        self.registry = registry

    def run(self, *, wf: WorkflowSpec, run_id: str, org_id: str, artifacts_root: str, state_root: str) -> RunSummary:
        artifacts = RunArtifacts(run_id=run_id, root_dir=artifacts_root)
        state = FileStateStore(root_dir=state_root)
        events = EventLogger(path=artifacts.events_path)
        ctx = RunContext(
            run_id=run_id,
            org_id=org_id,
            artifacts=artifacts,
            state=state,
            events=events,
            env=dict(os.environ),
        )

        artifacts.write_json("run.json", {"run_id": run_id, "org_id": org_id, "workflow_id": wf.workflow_id})
        events.emit("run_started", {"run_id": run_id, "org_id": org_id, "workflow_id": wf.workflow_id})

        tasks_by_id = {t.id: t for t in wf.tasks}
        order = _toposort([{"id": t.id, "depends_on": t.depends_on} for t in wf.tasks])

        task_results: Dict[str, Any] = {}
        ok = True

        for task_id in order:
            spec = tasks_by_id[task_id]
            task = self.registry.get(spec.type)
            events.emit("task_started", {"run_id": run_id, "task_id": task_id, "type": spec.type})

            if spec.idempotency_key:
                cached = state.get_idempotent_result(spec.idempotency_key)
                if cached is not None:
                    task_results[task_id] = {"ok": True, "cached": True, **cached}
                    artifacts.write_json(f"tasks/{task_id}/result.json", task_results[task_id])
                    events.emit("task_cached", {"run_id": run_id, "task_id": task_id, "idempotency_key": spec.idempotency_key})
                    continue

            def _do():
                return task.run(ctx=ctx, task_id=task_id, inputs=spec.inputs)

            try:
                res = run_with_retries(_do, spec.retry)
                task_results[task_id] = {"ok": bool(res.ok), "outputs": res.outputs, "summary": res.summary}
                artifacts.write_json(f"tasks/{task_id}/result.json", task_results[task_id])

                if spec.idempotency_key and res.ok:
                    state.put_idempotent_result(spec.idempotency_key, {"outputs": res.outputs, "summary": res.summary})

                events.emit("task_finished", {"run_id": run_id, "task_id": task_id, "ok": bool(res.ok)})
                if not res.ok:
                    ok = False
                    break
            except Exception as e:  # noqa: BLE001
                ok = False
                task_results[task_id] = {"ok": False, "error": str(e)}
                artifacts.write_json(f"tasks/{task_id}/result.json", task_results[task_id])
                events.emit("task_failed", {"run_id": run_id, "task_id": task_id, "error": str(e)})
                break

        state.write_run_summary(run_id, {"run_id": run_id, "org_id": org_id, "workflow_id": wf.workflow_id, "ok": ok, "tasks": task_results})
        events.emit("run_finished", {"run_id": run_id, "ok": ok})

        return RunSummary(run_id=run_id, org_id=org_id, workflow_id=wf.workflow_id, ok=ok, tasks=task_results)
