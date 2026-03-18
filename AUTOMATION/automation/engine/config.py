from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Defaults assume you run from the `AUTOMATION/` directory:
    # `cd AUTOMATION; python -m automation ...`
    artifacts_dir: str = "artifacts"
    state_dir: str = "state"
    log_level: str = "INFO"


def load_settings() -> Settings:
    return Settings(
        artifacts_dir=os.getenv("AUTO_ARTIFACTS_DIR", "artifacts"),
        state_dir=os.getenv("AUTO_STATE_DIR", "state"),
        log_level=os.getenv("AUTO_LOG_LEVEL", "INFO"),
    )
