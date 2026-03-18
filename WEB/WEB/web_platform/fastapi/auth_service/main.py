from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from fastapi import FastAPI, HTTPException

from web_platform.shared.auth.jwt_hs256 import encode
from web_platform.shared.auth.passwords import hash_password, verify_password
from web_platform.shared.config.env import load_settings


settings = load_settings()
app = FastAPI(title="WEB Auth Service", version="0.1.0")


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    role: str = "owner"
    plan: str = "free"


_USERS_BY_EMAIL: Dict[str, User] = {}


@app.post("/signup")
def signup(payload: dict):
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    if not email or not password:
        raise HTTPException(400, "email and password required")
    if email in _USERS_BY_EMAIL:
        raise HTTPException(409, "user already exists")
    u = User(id=email, email=email, password_hash=hash_password(password))
    _USERS_BY_EMAIL[email] = u
    return {"ok": True, "user": {"id": u.id, "email": u.email}}


@app.post("/login")
def login(payload: dict):
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    u = _USERS_BY_EMAIL.get(email)
    if not u or not verify_password(password, u.password_hash):
        raise HTTPException(401, "invalid credentials")
    token = encode({"sub": u.id, "email": u.email, "role": u.role, "plan": u.plan}, settings.secret_key, exp_seconds=3600)
    refresh = encode({"sub": u.id, "type": "refresh"}, settings.secret_key, exp_seconds=7 * 24 * 3600)
    return {"ok": True, "access_token": token, "refresh_token": refresh}






