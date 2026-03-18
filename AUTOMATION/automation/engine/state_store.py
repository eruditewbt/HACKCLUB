from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class FileStateStore:
    root_dir: str

    def _runs_dir(self) -> str:
        return os.path.join(self.root_dir, "runs")

    def _idemp_dir(self) -> str:
        return os.path.join(self.root_dir, "idempotency")

    def write_run_summary(self, run_id: str, summary: Dict[str, Any]) -> str:
        os.makedirs(self._runs_dir(), exist_ok=True)
        path = os.path.join(self._runs_dir(), f"{run_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=True)
        return path

    def read_run_summary(self, run_id: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(self._runs_dir(), f"{run_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_idempotent_result(self, key: str) -> Optional[Dict[str, Any]]:
        os.makedirs(self._idemp_dir(), exist_ok=True)
        path = os.path.join(self._idemp_dir(), f"{key}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def put_idempotent_result(self, key: str, result: Dict[str, Any]) -> str:
        os.makedirs(self._idemp_dir(), exist_ok=True)
        path = os.path.join(self._idemp_dir(), f"{key}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=True)
        return path
