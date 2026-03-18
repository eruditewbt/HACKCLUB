from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from typing import Any, Dict

from automation.engine.task import TaskResult


@dataclass(frozen=True)
class HttpCheckTask:
    type: str = "web.http_check"

    def run(self, *, ctx, task_id: str, inputs: Dict[str, Any]) -> TaskResult:
        url = str(inputs.get("url") or "").strip()
        if not url:
            return TaskResult(ok=False, outputs={}, summary="Missing url")

        expected_status = int(inputs.get("expected_status", 200))
        contains = inputs.get("contains")
        timeout_s = int(inputs.get("timeout_s", 10))

        req = urllib.request.Request(url, headers={"User-Agent": "automation-os/0.1"}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                status = int(resp.status)
                body = resp.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            ctx.artifacts.write_text(f"tasks/{task_id}/error.txt", str(e))
            return TaskResult(ok=False, outputs={"url": url, "error": str(e)}, summary="Network error")

        ok = status == expected_status
        if ok and contains is not None:
            ok = str(contains) in body

        ctx.artifacts.write_text(f"tasks/{task_id}/response.txt", body[:20000])

        return TaskResult(
            ok=ok,
            outputs={"url": url, "status": status, "expected_status": expected_status, "contains": contains},
            summary=("OK" if ok else "FAILED"),
        )
