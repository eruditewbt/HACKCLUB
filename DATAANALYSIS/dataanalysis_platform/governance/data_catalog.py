from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dataanalysis_platform.core.timeutils import iso_utc_now


@dataclass
class DatasetRecord:
    dataset_id: str
    name: str
    description: str
    owner: str
    tags: List[str]
    created_at: str
    updated_at: str
    schema: Dict[str, Any]
    source: Dict[str, Any]


class DataCatalog:
    """Tiny file-based catalog (upgrade to Postgres later).

    Monetizable direction: governance, ownership, trust, and discoverability.
    """

    def __init__(self, path: str = "catalog.json") -> None:
        self.path = path
        self._data: Dict[str, Any] = {"datasets": {}}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=True)

    def register_dataset(
        self,
        *,
        dataset_id: str,
        name: str,
        description: str = "",
        owner: str = "",
        tags: Optional[List[str]] = None,
        schema: Optional[Dict[str, Any]] = None,
        source: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        now = iso_utc_now()
        tags = tags or []
        schema = schema or {}
        source = source or {}

        existing = self._data["datasets"].get(dataset_id)
        created_at = existing.get("created_at") if existing else now

        rec = {
            "dataset_id": dataset_id,
            "name": name,
            "description": description,
            "owner": owner,
            "tags": tags,
            "created_at": created_at,
            "updated_at": now,
            "schema": schema,
            "source": source,
        }
        self._data["datasets"][dataset_id] = rec
        self._save()
        return rec

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        return self._data["datasets"].get(dataset_id)

    def list_datasets(self) -> List[Dict[str, Any]]:
        return list(self._data["datasets"].values())
