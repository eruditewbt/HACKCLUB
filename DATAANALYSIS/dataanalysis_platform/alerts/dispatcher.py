from __future__ import annotations

import os
from typing import Any, Dict, Optional

from dataanalysis_platform.alerts.webhook import post_json


def dispatch_validation_alert(
    *,
    webhook_url: Optional[str],
    event: Dict[str, Any],
) -> None:
    url = (webhook_url or os.getenv("DA_WEBHOOK_URL_DEFAULT") or "").strip()
    if not url:
        return

    # Best-effort: alerts should never crash the pipeline.
    try:
        post_json(url, event)
    except Exception:
        return
