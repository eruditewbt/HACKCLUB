from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from automation.engine.artifacts import RunArtifacts
from automation.engine.observability import EventLogger
from automation.engine.state_store import FileStateStore


@dataclass
class RunContext:
    run_id: str
    org_id: str
    artifacts: RunArtifacts
    state: FileStateStore
    events: EventLogger
    env: Dict[str, str]
