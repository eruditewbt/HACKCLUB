from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    index: int
    text: str


def _normalize_whitespace(s: str) -> str:
    return "\n".join([" ".join(line.split()) for line in s.splitlines()]).strip()


def chunk_text(
    *,
    doc_id: str,
    text: str,
    max_chars: int = 1200,
    overlap_chars: int = 150,
) -> List[Chunk]:
    text = text or ""
    text = text.replace("\r\n", "\n")

    # Prefer paragraph boundaries.
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paras:
        paras = [text.strip()] if text.strip() else []

    # Build chunks by concatenating paragraphs.
    chunks: List[str] = []
    buf = ""
    for p in paras:
        p = _normalize_whitespace(p)
        if not p:
            continue
        if not buf:
            buf = p
            continue
        if len(buf) + 2 + len(p) <= max_chars:
            buf = buf + "\n\n" + p
        else:
            chunks.append(buf)
            buf = p
    if buf:
        chunks.append(buf)

    # Enforce max_chars even for a single huge paragraph.
    final: List[str] = []
    for c in chunks:
        if len(c) <= max_chars:
            final.append(c)
            continue
        start = 0
        while start < len(c):
            end = min(len(c), start + max_chars)
            final.append(c[start:end])
            if end >= len(c):
                break
            start = max(0, end - overlap_chars)

    out: List[Chunk] = []
    for i, c in enumerate(final):
        out.append(Chunk(chunk_id=f"{doc_id}:{i}", index=i, text=c))
    return out
