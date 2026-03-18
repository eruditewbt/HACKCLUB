from __future__ import annotations

import json
import os
import tempfile
from typing import Any, Dict, Optional

from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from dataanalysis_platform.artifacts.db import make_engine
from dataanalysis_platform.pipelines.orchestration import run_pipeline_csv
from dataanalysis_platform.profiling.drift import detect_drift


app = FastAPI(title="DATAANALYSIS Analytics API", version="0.2.1")


def _require_org_id(x_org_id: Optional[str]) -> str:
    org = (x_org_id or "").strip()
    if not org:
        raise HTTPException(status_code=400, detail="Missing X-Org-ID header")
    return org


def _read_json_upload(file: UploadFile) -> Dict[str, Any]:
    try:
        raw = file.file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return json.loads(raw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")


def _repo_or_501():
    try:
        from dataanalysis_platform.artifacts.repository import (
            get_latest_two_profiles,
            get_report_html,
            init_db,
            list_runs,
        )

        return get_latest_two_profiles, get_report_html, init_db, list_runs
    except Exception:
        raise HTTPException(status_code=501, detail="Persistence layer unavailable (install requirements + set DATABASE_URL)")


@app.get("/health")
async def health() -> JSONResponse:
    engine = make_engine()
    return JSONResponse({"ok": True, "db": bool(engine is not None)})


@app.post("/run")
async def run(
    csv: UploadFile = File(...),
    rules: Optional[UploadFile] = File(None),
    dataset_name: str = Form("dataset"),
    webhook_url: Optional[str] = Form(None),
    max_rows: Optional[int] = Form(None),
    x_org_id: Optional[str] = Header(None),
) -> JSONResponse:
    org_id = _require_org_id(x_org_id)

    if not (csv.filename or "").lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a .csv file")

    rules_spec = _read_json_upload(rules) if rules is not None else None

    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "upload.csv")
        with open(path, "wb") as f:
            f.write(await csv.read())

        art = run_pipeline_csv(
            csv_path=path,
            rules_spec=rules_spec,
            artifacts_dir="artifacts",
            max_rows=max_rows,
            org_id=org_id,
            dataset_name=dataset_name,
            webhook_url=webhook_url,
            persist=True,
            title=f"Data Health Report: {dataset_name}",
        )

        return JSONResponse(
            {
                "run_id": art["run_id"],
                "org_id": org_id,
                "dataset_name": dataset_name,
                "artifact": art["artifact_path"],
                "report_url": f"/report/{art['run_id']}",
                "quality_score": (art.get("validation") or {}).get("quality_score"),
            }
        )


@app.get("/report/{run_id}")
async def report(run_id: str, x_org_id: Optional[str] = Header(None)) -> HTMLResponse:
    org_id = _require_org_id(x_org_id)

    engine = make_engine()
    if engine is not None:
        _, get_report_html, init_db, _ = _repo_or_501()
        init_db(engine)
        html_doc = get_report_html(engine=engine, org_id=org_id, run_id=run_id)
        if html_doc is None:
            raise HTTPException(status_code=404, detail="Report not found")
        return HTMLResponse(html_doc)

    path = os.path.join("artifacts", f"{run_id}.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Report not found")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/runs")
async def runs(dataset_name: Optional[str] = None, limit: int = 50, x_org_id: Optional[str] = Header(None)) -> JSONResponse:
    org_id = _require_org_id(x_org_id)
    engine = make_engine()
    if engine is None:
        raise HTTPException(status_code=501, detail="DATABASE_URL not configured")
    _, _, init_db, list_runs = _repo_or_501()
    init_db(engine)
    return JSONResponse({"runs": list_runs(engine=engine, org_id=org_id, dataset_name=dataset_name, limit=limit)})


@app.get("/drift/{dataset_name}")
async def drift(dataset_name: str, x_org_id: Optional[str] = Header(None)) -> JSONResponse:
    org_id = _require_org_id(x_org_id)
    engine = make_engine()
    if engine is None:
        raise HTTPException(status_code=501, detail="DATABASE_URL not configured")

    get_latest_two_profiles, _, init_db, _ = _repo_or_501()
    init_db(engine)

    profiles = get_latest_two_profiles(engine=engine, org_id=org_id, dataset_name=dataset_name)
    if len(profiles) < 2:
        raise HTTPException(status_code=400, detail="Need at least two stored runs for drift detection")

    current = profiles[0]
    previous = profiles[1]
    findings = detect_drift(previous_profile=previous, current_profile=current)

    return JSONResponse({"dataset_name": dataset_name, "findings": findings})
