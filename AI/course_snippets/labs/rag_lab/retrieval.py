from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from .chunking import Chunk


_TOK_RE = re.compile(r"[A-Za-z0-9']+")


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOK_RE.findall(text or "")]


@dataclass
class CorpusIndex:
    chunks: List[Chunk]
    df: Dict[str, int]
    n_docs: int
    chunk_tf: List[Counter]


def build_index(chunks: List[Chunk]) -> CorpusIndex:
    df: Dict[str, int] = defaultdict(int)
    chunk_tf: List[Counter] = []
    for ch in chunks:
        tf = Counter(tokenize(ch.text))
        chunk_tf.append(tf)
        for term in set(tf.keys()):
            df[term] += 1
    return CorpusIndex(chunks=chunks, df=dict(df), n_docs=len(chunks), chunk_tf=chunk_tf)


def score_tfidf(index: CorpusIndex, query: str, k: int = 3) -> List[Tuple[float, Chunk]]:
    q = Counter(tokenize(query))
    if not q:
        return []
    scores: List[Tuple[float, int]] = []
    for i, tf in enumerate(index.chunk_tf):
        score = 0.0
        for term, qcnt in q.items():
            if term not in tf:
                continue
            # smooth idf
            idf = math.log((index.n_docs + 1) / (index.df.get(term, 0) + 1)) + 1.0
            score += (tf[term] * idf) * qcnt
        if score > 0.0:
            scores.append((score, i))
    scores.sort(key=lambda t: t[0], reverse=True)
    return [(s, index.chunks[i]) for s, i in scores[:k]]


