from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + pad).encode("ascii"))


def encode(payload: Dict[str, Any], secret: str, exp_seconds: int = 3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    body = dict(payload)
    body.setdefault("iat", now)
    body.setdefault("exp", now + exp_seconds)
    segments = [
        _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8")),
        _b64url(json.dumps(body, separators=(",", ":")).encode("utf-8")),
    ]
    signing_input = ".".join(segments).encode("ascii")
    sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    segments.append(_b64url(sig))
    return ".".join(segments)


class JwtError(Exception):
    pass


def decode(token: str, secret: str) -> Dict[str, Any]:
    try:
        h, p, s = token.split(".", 2)
    except ValueError:
        raise JwtError("Invalid token format")
    signing_input = f"{h}.{p}".encode("ascii")
    sig = _b64url_decode(s)
    expected = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, expected):
        raise JwtError("Bad signature")
    payload = json.loads(_b64url_decode(p).decode("utf-8"))
    now = int(time.time())
    if "exp" in payload and int(payload["exp"]) < now:
        raise JwtError("Token expired")
    return payload


