from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol


@dataclass
class TaskResult:
    ok: bool
    outputs: Dict[str, Any]
    summary: str = ""


class Task(Protocol):
    type: str

    def run(self, *, ctx: "RunContext", task_id: str, inputs: Dict[str, Any]) -> TaskResult:
        ...


class RunContext:  # pragma: no cover
    ...
