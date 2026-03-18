from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class IdempotencyRecord:
    key: str
    created_at: float


class InMemoryIdempotencyStore:
    def __init__(self, ttl_s: int = 3600):
        self.ttl_s = ttl_s
        self._items: Dict[str, IdempotencyRecord] = {}

    def seen(self, key: str) -> bool:
        self._gc()
        return key in self._items

    def mark(self, key: str) -> None:
        self._gc()
        self._items[key] = IdempotencyRecord(key=key, created_at=time.time())

    def _gc(self) -> None:
        now = time.time()
        dead = [k for k, v in self._items.items() if now - v.created_at > self.ttl_s]
        for k in dead:
            self._items.pop(k, None)


