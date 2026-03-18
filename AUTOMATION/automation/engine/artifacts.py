from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class RunArtifacts:
    run_id: str
    root_dir: str

    @property
    def run_dir(self) -> str:
        return os.path.join(self.root_dir, self.run_id)

    @property
    def events_path(self) -> str:
        return os.path.join(self.run_dir, "events.jsonl")

    def task_dir(self, task_id: str) -> str:
        return os.path.join(self.run_dir, "tasks", task_id)

    def write_json(self, rel_path: str, obj: Dict[str, Any]) -> str:
        path = os.path.join(self.run_dir, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=True)
        return path

    def write_text(self, rel_path: str, text: str) -> str:
        path = os.path.join(self.run_dir, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path
