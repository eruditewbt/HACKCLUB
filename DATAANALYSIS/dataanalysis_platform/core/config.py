from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    artifacts_dir: str = "artifacts"
    max_rows_default: int = 200_000


def load_settings() -> Settings:
    artifacts_dir = os.getenv("DA_ARTIFACTS_DIR", "artifacts")
    max_rows_default = int(os.getenv("DA_MAX_ROWS_DEFAULT", "200000"))
    return Settings(artifacts_dir=artifacts_dir, max_rows_default=max_rows_default)
