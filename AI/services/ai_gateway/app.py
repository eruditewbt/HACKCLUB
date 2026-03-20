from __future__ import annotations

from typing import Any, Dict, Optional

from ai_platform.core.config import load_settings
from ai_platform.rag.answer import synthesize_answer
from ai_platform.rag.rag_pipeline import RagPipeline
from ai_platform.rag.sqlite_store import SqliteRagStore

try:
    from fastapi import FastAPI, Header, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "FastAPI dependencies are not installed. Install fastapi + uvicorn + pydantic to run the gateway.\n"
        f"Import error: {e}"
    )


app = FastAPI(title="AI Gateway", version="0.1.0")
settings = load_settings()
pipe = RagPipeline(store=SqliteRagStore(path=settings.db_path), settings=settings)
pipe.init()


def _org(x_org_id: Optional[str]) -> str:
    org_id = (x_org_id or "default").strip()
    if not org_id:
        raise HTTPException(status_code=400, detail="Invalid X-Org-ID")
    return org_id


class IngestRequest(BaseModel):
    doc_id: str
    title: str
    text: str
    metadata: Dict[str, Any] = {}


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"ok": True})


@app.post("/ingest")
def ingest(req: IngestRequest, x_org_id: Optional[str] = Header(None)) -> JSONResponse:
    org_id = _org(x_org_id)
    res = pipe.ingest_text(org_id=org_id, doc_id=req.doc_id, title=req.title, text=req.text, metadata=req.metadata)
    return JSONResponse(res)


@app.post("/search")
def search(req: SearchRequest, x_org_id: Optional[str] = Header(None)) -> JSONResponse:
    org_id = _org(x_org_id)
    hits = pipe.search(org_id=org_id, query=req.query, top_k=req.top_k)
    return JSONResponse({"hits": hits})


@app.post("/answer")
def answer(req: SearchRequest, x_org_id: Optional[str] = Header(None)) -> JSONResponse:
    org_id = _org(x_org_id)
    hits = pipe.search(org_id=org_id, query=req.query, top_k=req.top_k)
    ans = synthesize_answer(query=req.query, hits=hits)
    return JSONResponse({"answer": ans, "hits": hits})
