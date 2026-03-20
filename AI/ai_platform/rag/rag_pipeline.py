from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ai_platform.core.config import Settings
from ai_platform.core.timeutils import iso_utc_now
from ai_platform.rag.chunking import chunk_text
from ai_platform.rag.sqlite_store import SqliteRagStore
from ai_platform.security.pii import redact_pii


@dataclass
class RagPipeline:
    store: SqliteRagStore
    settings: Settings

    def init(self) -> None:
        self.store.init()

    def ingest_text(
        self,
        *,
        org_id: str,
        doc_id: str,
        title: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        redact: bool = True,
    ) -> Dict[str, Any]:
        metadata = metadata or {}
        created_at = iso_utc_now()
        clean = redact_pii(text) if redact else (text or "")
        chunks = chunk_text(
            doc_id=doc_id,
            text=clean,
            max_chars=self.settings.max_chunk_chars,
            overlap_chars=self.settings.chunk_overlap_chars,
        )

        self.store.upsert_doc(org_id=org_id, doc_id=doc_id, title=title, metadata=metadata, created_at=created_at)
        self.store.replace_chunks(
            org_id=org_id,
            doc_id=doc_id,
            chunks=[(c.chunk_id, c.index, c.text) for c in chunks],
            created_at=created_at,
        )
        return {"org_id": org_id, "doc_id": doc_id, "title": title, "chunks": len(chunks), "created_at": created_at}

    def search(self, *, org_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return self.store.search(org_id=org_id, query=query, top_k=top_k)
