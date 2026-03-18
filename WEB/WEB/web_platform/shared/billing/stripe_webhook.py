from __future__ import annotations

import hashlib
import hmac
import time


class WebhookError(Exception):
    pass


def verify_stripe_signature(payload: bytes, sig_header: str, signing_secret: str, tolerance_s: int = 300) -> None:
    """
    Stripe-style signature: "t=timestamp,v1=hexsig"
    Signature = HMAC_SHA256(secret, f"{t}.{payload}")
    """
    parts = {}
    for piece in (sig_header or "").split(","):
        if "=" in piece:
            k, v = piece.split("=", 1)
            parts[k.strip()] = v.strip()
    if "t" not in parts or "v1" not in parts:
        raise WebhookError("Missing stripe signature fields")
    t = int(parts["t"])
    if abs(int(time.time()) - t) > tolerance_s:
        raise WebhookError("Timestamp outside tolerance")
    signed = f"{t}.".encode("utf-8") + payload
    expected = hmac.new(signing_secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, parts["v1"]):
        raise WebhookError("Invalid signature")


