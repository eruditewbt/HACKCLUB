from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any, Dict

from automation.engine.task import TaskResult


@dataclass(frozen=True)
class DataHealthRunTask:
    """Bridge into the external DATAANALYSIS project via CLI."""

    type: str = "data.health_run"

    def run(self, *, ctx, task_id: str, inputs: Dict[str, Any]) -> TaskResult:
        da_root = (inputs.get("dataanalysis_root") or os.getenv("DATAANALYSIS_ROOT") or "").strip()
        if not da_root:
            return TaskResult(ok=False, outputs={}, summary="Missing DATAANALYSIS_ROOT")

        csv_path = str(inputs.get("csv_path") or "").strip()
        rules_path = str(inputs.get("rules_path") or "").strip()
        org_id = str(inputs.get("org_id") or ctx.org_id)
        dataset = str(inputs.get("dataset") or "dataset")
        out_dir = str(inputs.get("out_dir") or ctx.artifacts.task_dir(task_id))

        cmd = [
            "python",
            "-m",
            "dataanalysis_platform",
            "run-all",
            "--input",
            csv_path,
            "--rules",
            rules_path,
            "--org-id",
            org_id,
            "--dataset",
            dataset,
            "--out",
            out_dir,
            "--no-persist",
        ]

        proc = subprocess.run(cmd, cwd=da_root, capture_output=True, text=True, check=False)

        ctx.artifacts.write_text(f"tasks/{task_id}/stdout.txt", proc.stdout)
        ctx.artifacts.write_text(f"tasks/{task_id}/stderr.txt", proc.stderr)

        ok = proc.returncode == 0
        outputs: Dict[str, Any] = {
            "returncode": proc.returncode,
            "cmd": cmd,
            "dataanalysis_root": da_root,
            "dataset": dataset,
            "org_id": org_id,
            "out_dir": out_dir,
        }

        for line in reversed(proc.stdout.splitlines()):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    outputs["dataanalysis_result"] = json.loads(line)
                except Exception:
                    pass
                break

        return TaskResult(ok=ok, outputs=outputs, summary=("OK" if ok else "FAILED"))
