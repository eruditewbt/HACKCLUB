from __future__ import annotations

import os
from dataclasses import dataclass


def _get(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v


def _get_int(name: str, default: int) -> int:
    v = _get(name)
    if v is None:
        return default
    try:
        return int(v)
    except ValueError:
        return default


def _get_bool(name: str, default: bool) -> bool:
    v = _get(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    env: str
    secret_key: str
    database_url: str
    redis_url: str

    api_rate_limit_rpm: int
    enable_cors: bool
    cors_allow_origins: str


def load_settings(prefix: str = "WEB_") -> Settings:
    env = _get(prefix + "ENV", "dev") or "dev"
    secret_key = _get(prefix + "SECRET_KEY", "dev-secret-change-me") or "dev-secret-change-me"
    database_url = _get(prefix + "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/web") or ""
    redis_url = _get(prefix + "REDIS_URL", "redis://localhost:6379/0") or ""
    api_rate_limit_rpm = _get_int(prefix + "RATE_LIMIT_RPM", 120)
    enable_cors = _get_bool(prefix + "CORS", True)
    cors_allow_origins = _get(prefix + "CORS_ALLOW_ORIGINS", "*") or "*"
    return Settings(
        env=env,
        secret_key=secret_key,
        database_url=database_url,
        redis_url=redis_url,
        api_rate_limit_rpm=api_rate_limit_rpm,
        enable_cors=enable_cors,
        cors_allow_origins=cors_allow_origins,
    )


