from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict


def iso_utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@dataclass
class EventLogger:
    path: str

    def emit(self, event: str, payload: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        rec = {"ts": iso_utc_now(), "event": event, **payload}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")
