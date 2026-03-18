from __future__ import annotations

from flask import Flask, request

from web_platform.shared.billing.stripe_webhook import WebhookError, verify_stripe_signature
from web_platform.shared.config.env import load_settings
from web_platform.shared.utils.idempotency import InMemoryIdempotencyStore


settings = load_settings()
app = Flask(__name__)
idem = InMemoryIdempotencyStore(ttl_s=3600)


@app.post("/webhooks/stripe")
def stripe_webhook():
    sig = request.headers.get("stripe-signature")
    if not sig:
        return {"ok": False, "error": "missing stripe-signature"}, 400
    payload = request.get_data() or b""
    try:
        verify_stripe_signature(payload, sig, settings.secret_key)
    except WebhookError as e:
        return {"ok": False, "error": str(e)}, 400
    idem_key = request.headers.get("x-idempotency-key")
    if idem_key:
        if idem.seen(idem_key):
            return {"ok": True, "deduped": True}
        idem.mark(idem_key)
    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)






