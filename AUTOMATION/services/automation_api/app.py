from __future__ import annotations

import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional

from automation.engine.config import load_settings
from automation.engine.runner import WorkflowRunner
from automation.engine.state_store import FileStateStore
from automation.engine.workflow import load_workflow
from automation.tasks import default_registry

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "FastAPI service dependencies are not installed. "
        "Install fastapi + uvicorn to use AUTOMATION/services/automation_api.\n"
        f"Import error: {e}"
    )


app = FastAPI(title="Automation OS API", version="0.2.0")
settings = load_settings()
state = FileStateStore(root_dir=settings.state_dir)
runner = WorkflowRunner(registry=default_registry())

# Basic in-process async execution for demos. Upgrade to a real queue later.
_executor = ThreadPoolExecutor(max_workers=int(os.getenv("AUTO_API_WORKERS", "4")))


class RunRequest(BaseModel):
    workflow_path: str
    org_id: str = "default"
    run_id: Optional[str] = None


def _safe_resolve_workflow(path: str) -> str:
    # Prevent path traversal. Allow only paths under AUTOMATION/workflows/ or absolute paths.
    p = os.path.normpath(path)
    if os.path.isabs(p):
        return p
    # Relative paths are resolved relative to the current working dir.
    # For production you might want a fixed base directory.
    if ".." in p.split(os.sep):
        raise HTTPException(status_code=400, detail="Invalid workflow_path")
    return p


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"ok": True})


@app.post("/run")
def run(req: RunRequest) -> JSONResponse:
    run_id = req.run_id or uuid.uuid4().hex
    wf_path = _safe_resolve_workflow(req.workflow_path)

    try:
        wf = load_workflow(wf_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load workflow: {e}")

    def _job() -> None:
        runner.run(
            wf=wf,
            run_id=run_id,
            org_id=req.org_id,
            artifacts_root=settings.artifacts_dir,
            state_root=settings.state_dir,
        )

    _executor.submit(_job)
    return JSONResponse({"run_id": run_id, "queued": True})


@app.get("/status/{run_id}")
def status(run_id: str) -> JSONResponse:
    data = state.read_run_summary(run_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return JSONResponse(data)


@app.get("/artifacts/{run_id}")
def artifacts(run_id: str) -> JSONResponse:
    # Returns the artifact directory path and a shallow listing.
    run_dir = os.path.join(settings.artifacts_dir, run_id)
    if not os.path.isdir(run_dir):
        raise HTTPException(status_code=404, detail="Artifacts not found")

    items = []
    for name in sorted(os.listdir(run_dir)):
        p = os.path.join(run_dir, name)
        items.append({"name": name, "is_dir": os.path.isdir(p)})

    return JSONResponse({"run_id": run_id, "run_dir": run_dir, "items": items})

