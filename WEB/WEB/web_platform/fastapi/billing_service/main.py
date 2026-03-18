from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, Request

from web_platform.shared.billing.plans import PLANS
from web_platform.shared.billing.stripe_webhook import WebhookError, verify_stripe_signature
from web_platform.shared.config.env import load_settings
from web_platform.shared.utils.idempotency import InMemoryIdempotencyStore


settings = load_settings()
app = FastAPI(title="WEB Billing Service", version="0.1.0")
idem = InMemoryIdempotencyStore(ttl_s=3600)


@app.get("/plans")
def list_plans():
    return {"plans": [p.__dict__ for p in PLANS.values()]}


@app.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="stripe-signature"),
    x_idempotency_key: str | None = Header(default=None, alias="x-idempotency-key"),
):
    payload = await request.body()
    if not stripe_signature:
        raise HTTPException(400, "missing stripe-signature header")
    signing_secret = settings.secret_key  # for demo; use STRIPE_SIGNING_SECRET in production
    try:
        verify_stripe_signature(payload, stripe_signature, signing_secret)
    except WebhookError as e:
        raise HTTPException(400, str(e))

    if x_idempotency_key:
        if idem.seen(x_idempotency_key):
            return {"ok": True, "deduped": True}
        idem.mark(x_idempotency_key)

    # TODO: parse event JSON, update subscription state machine, write audit log
    return {"ok": True, "accepted": True}






