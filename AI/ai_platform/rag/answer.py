from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List


def _sentences(text: str) -> List[str]:
    """Deterministic splitter that works for paragraphs and bullet lists."""
    t = (text or "").replace("\r\n", "\n").strip()
    if not t:
        return []

    parts: List[str] = []
    for line in t.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Keep bullet lines as their own sentences (common in docs).
        if line.startswith(("-", "*")):
            parts.append(line.lstrip("-* ").strip())
            continue
        parts.append(line)

    out: List[str] = []
    for p in parts:
        raw = re.split(r"(?<=[.!?])\s+", p.strip())
        out.extend([s.strip() for s in raw if s.strip()])
    return out


def _score_sentence(sent: str, q_terms: List[str]) -> int:
    s = sent.lower()
    score = 0
    for t in q_terms:
        if t and t in s:
            score += 1
    return score


def synthesize_answer(*, query: str, hits: List[Dict[str, Any]], max_sentences: int = 6) -> Dict[str, Any]:
    base_terms = [t for t in re.findall(r"[a-z0-9]{3,}", (query or "").lower())]
    # Add simple singular/plural normalization to improve matching in bullet lists.
    q_terms = set(base_terms)
    for t in list(q_terms):
        if t.endswith("s") and len(t) > 3:
            q_terms.add(t[:-1])
        else:
            q_terms.add(t + "s")
    q_terms = sorted(q_terms)

    # Build a pool of candidate sentences from top hits.
    pool = []
    for h in hits:
        for s in _sentences(h.get("text") or ""):
            pool.append((h.get("chunk_id"), s, _score_sentence(s, q_terms)))

    pool.sort(key=lambda x: (-x[2], len(x[1])))

    chosen = []
    used = set()
    for chunk_id, sent, sc in pool:
        if sc <= 0:
            continue
        if sent in used:
            continue
        used.add(sent)
        chosen.append(sent)
        if len(chosen) >= max_sentences:
            break

    if not chosen:
        # Fallback: first sentences from first hit.
        if hits:
            sents = _sentences(hits[0].get("text") or "")
            chosen = sents[: min(max_sentences, len(sents))]

    answer = " ".join(chosen).strip()

    citations = []
    for h in hits:
        citations.append({"chunk_id": h.get("chunk_id"), "doc_id": h.get("doc_id"), "score": h.get("score")})

    return {"answer": answer, "citations": citations}
