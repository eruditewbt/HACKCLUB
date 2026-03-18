from __future__ import annotations

from fastapi import FastAPI, HTTPException


app = FastAPI(title="WEB Analytics Service", version="0.1.0")


@app.post("/events")
def ingest(payload: dict):
    if "event" not in payload:
        raise HTTPException(400, "missing event")
    # TODO: store into DB, aggregate, expose dashboards
    return {"ok": True}


