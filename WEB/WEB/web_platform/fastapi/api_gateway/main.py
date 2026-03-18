from __future__ import annotations

import logging
import time
from typing import Dict, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from web_platform.shared.auth.jwt_hs256 import JwtError, decode
from web_platform.shared.billing.plans import get_plan
from web_platform.shared.config.env import load_settings
from web_platform.shared.observability.logging import setup_json_logging
from web_platform.shared.observability.request_id import new_request_id
from web_platform.shared.security.headers import security_headers


settings = load_settings()
setup_json_logging("INFO")
log = logging.getLogger("web.gateway")

app = FastAPI(title="WEB API Gateway", version="0.1.0")

if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_allow_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


_RPM_BUCKET: Dict[str, list[float]] = {}  # api_key -> request timestamps (dev-only)


@app.middleware("http")
async def request_context(request: Request, call_next):
    rid = request.headers.get("x-request-id") or new_request_id()
    request.state.request_id = rid
    start = time.time()
    resp = await call_next(request)
    for k, v in security_headers().items():
        resp.headers.setdefault(k, v)
    resp.headers["x-request-id"] = rid
    log.info("request complete", extra={"request_id": rid})
    resp.headers["x-response-time-ms"] = str(int((time.time() - start) * 1000))
    return resp


def _rate_limit(api_key: str, rpm: int) -> None:
    now = time.time()
    window = 60.0
    bucket = _RPM_BUCKET.setdefault(api_key, [])
    # keep last minute
    bucket[:] = [t for t in bucket if now - t <= window]
    if len(bucket) >= rpm:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    bucket.append(now)


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> str:
    # In production: validate against DB, check revocation, etc.
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    return x_api_key


def require_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        return decode(token, settings.secret_key)
    except JwtError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/v1/billing/plans")
def plans():
    # Public endpoint: ok to expose plan metadata
    return {"plans": [p.__dict__ for p in [get_plan("free"), get_plan("pro"), get_plan("business")] if p]}


@app.post("/v1/usage/events")
def usage_event(payload: dict, api_key: str = Depends(require_api_key)):
    # Minimal metering hook
    plan = get_plan("free")
    _rate_limit(api_key, rpm=(plan.rpm_limit if plan else settings.api_rate_limit_rpm))
    return {"ok": True, "ingested": True}


@app.post("/v1/auth/whoami")
def whoami(user=Depends(require_user)):
    return {"ok": True, "claims": user}


@app.exception_handler(HTTPException)
async def http_exc(_req: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"ok": False, "error": exc.detail})






