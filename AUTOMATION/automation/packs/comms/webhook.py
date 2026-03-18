from __future__ import annotations

import json
import os
import urllib.request
from typing import Any, Dict, Optional, Tuple


def post_json(url: str, payload: Dict[str, Any], *, timeout_s: int = 10) -> Tuple[int, str]:
    data = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "automation-os/0.1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return int(resp.status), body


def default_webhook_url() -> Optional[str]:
    url = os.getenv("AUTO_WEBHOOK_URL_DEFAULT", "").strip()
    return url or None
