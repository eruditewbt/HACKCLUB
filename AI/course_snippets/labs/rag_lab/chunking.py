from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    chunk_id: int
    text: str


def chunk_text(doc_id: str, text: str, chunk_size: int = 250, overlap: int = 40) -> List[Chunk]:
    text = (text or "").strip()
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    step = max(1, chunk_size - overlap)
    chunks: List[Chunk] = []
    i = 0
    cid = 0
    while i < len(text):
        chunk = text[i : i + chunk_size]
        chunks.append(Chunk(doc_id=doc_id, chunk_id=cid, text=chunk))
        cid += 1
        i += step
    return chunks


