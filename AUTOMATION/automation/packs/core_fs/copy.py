from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from typing import Any, Dict

from automation.engine.task import TaskResult


@dataclass(frozen=True)
class CopyFileTask:
    type: str = "fs.copy"

    def run(self, *, ctx, task_id: str, inputs: Dict[str, Any]) -> TaskResult:
        src = str(inputs.get("src") or "").strip()
        dst = str(inputs.get("dst") or "").strip()
        if not src or not dst:
            return TaskResult(ok=False, outputs={}, summary="Missing src/dst")
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(src, dst)
        return TaskResult(ok=True, outputs={"src": src, "dst": dst}, summary="Copied")
