from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_path: str = "ai_platform_state/ai_rag.sqlite"
    max_chunk_chars: int = 1200
    chunk_overlap_chars: int = 150


def load_settings() -> Settings:
    return Settings(
        db_path=os.getenv("AI_DB_PATH", "ai_platform_state/ai_rag.sqlite"),
        max_chunk_chars=int(os.getenv("AI_MAX_CHUNK_CHARS", "1200")),
        chunk_overlap_chars=int(os.getenv("AI_CHUNK_OVERLAP_CHARS", "150")),
    )
