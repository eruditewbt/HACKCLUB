from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from automation.engine.task import TaskResult


@dataclass(frozen=True)
class EchoTask:
    type: str = "core.echo"

    def run(self, *, ctx, task_id: str, inputs: Dict[str, Any]) -> TaskResult:
        msg = str(inputs.get("message") or "")
        ctx.artifacts.write_text(f"tasks/{task_id}/message.txt", msg)
        return TaskResult(ok=True, outputs={"message": msg}, summary="Echoed")
