from __future__ import annotations

import json
import os
import sqlite3
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from ai_platform.core.errors import StorageError


SCHEMA = r"""
CREATE TABLE IF NOT EXISTS docs(
  org_id TEXT NOT NULL,
  doc_id TEXT NOT NULL,
  title TEXT NOT NULL,
  metadata_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY(org_id, doc_id)
);

CREATE TABLE IF NOT EXISTS chunks(
  org_id TEXT NOT NULL,
  doc_id TEXT NOT NULL,
  chunk_id TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  text TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY(org_id, chunk_id)
);

-- FTS5 for content search. chunk_id is stored as UNINDEXED.
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  org_id UNINDEXED,
  doc_id UNINDEXED,
  chunk_id UNINDEXED,
  text,
  tokenize = 'porter'
);

CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(org_id, doc_id, chunk_index);
"""


@dataclass
class SqliteRagStore:
    path: str

    def _connect(self) -> sqlite3.Connection:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def init(self) -> None:
        try:
            with self._connect() as c:
                c.executescript(SCHEMA)
        except sqlite3.OperationalError as e:
            raise StorageError(
                "Failed to initialize SQLite store. "
                "Ensure your Python SQLite build supports FTS5. "
                f"Original error: {e}"
            )

    def upsert_doc(self, *, org_id: str, doc_id: str, title: str, metadata: Dict[str, Any], created_at: str) -> None:
        with self._connect() as c:
            c.execute(
                "INSERT OR REPLACE INTO docs(org_id, doc_id, title, metadata_json, created_at) VALUES (?,?,?,?,?)",
                (org_id, doc_id, title, json.dumps(metadata, ensure_ascii=True), created_at),
            )

    def replace_chunks(self, *, org_id: str, doc_id: str, chunks: List[Tuple[str, int, str]], created_at: str) -> None:
        with self._connect() as c:
            # delete existing
            c.execute("DELETE FROM chunks WHERE org_id=? AND doc_id=?", (org_id, doc_id))
            c.execute("DELETE FROM chunks_fts WHERE org_id=? AND doc_id=?", (org_id, doc_id))

            c.executemany(
                "INSERT INTO chunks(org_id, doc_id, chunk_id, chunk_index, text, created_at) VALUES (?,?,?,?,?,?)",
                [(org_id, doc_id, cid, idx, text, created_at) for (cid, idx, text) in chunks],
            )
            c.executemany(
                "INSERT INTO chunks_fts(org_id, doc_id, chunk_id, text) VALUES (?,?,?,?)",
                [(org_id, doc_id, cid, text) for (cid, idx, text) in chunks],
            )

    def search(self, *, org_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q_raw = (query or "").strip()
        if not q_raw:
            return []

        # SQLite FTS5 MATCH uses its own query syntax; natural language (e.g. '?')
        # will raise errors. Convert to a safe token query.
        tokens = re.findall(r"[a-z0-9]{2,}", q_raw.lower())
        if not tokens:
            return []
        q = " OR ".join(tokens[:24])

        with self._connect() as c:
            # bm25 lower is better
            rows = c.execute(
                """
                SELECT chunk_id, doc_id, text, bm25(chunks_fts) AS score
                FROM chunks_fts
                WHERE org_id=? AND chunks_fts MATCH ?
                ORDER BY score
                LIMIT ?
                """,
                (org_id, q, int(top_k)),
            ).fetchall()

        out = []
        for r in rows:
            out.append(
                {
                    "chunk_id": r["chunk_id"],
                    "doc_id": r["doc_id"],
                    "text": r["text"],
                    "score": float(r["score"]),
                }
            )
        return out
