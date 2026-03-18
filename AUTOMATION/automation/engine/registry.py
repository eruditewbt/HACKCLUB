from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from automation.engine.task import Task


@dataclass
class TaskRegistry:
    tasks: Dict[str, Task]

    def register(self, task: Task) -> None:
        self.tasks[getattr(task, "type")] = task

    def get(self, type_name: str) -> Task:
        if type_name not in self.tasks:
            raise KeyError(f"Unknown task type: {type_name}")
        return self.tasks[type_name]
