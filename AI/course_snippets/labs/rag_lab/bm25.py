import math
from collections import Counter

from course_snippets.labs.rag_lab.text import tokenize


def build_corpus_stats(docs):
    """
    Builds corpus stats for BM25-ish scoring.
    docs: list[str]
    """
    tokenized = [tokenize(d) for d in docs]
    doc_lens = [len(toks) for toks in tokenized]
    avgdl = (sum(doc_lens) / len(doc_lens)) if doc_lens else 0.0

    df = Counter()
    for toks in tokenized:
        for t in set(toks):
            df[t] += 1

    return {"tokenized": tokenized, "doc_lens": doc_lens, "avgdl": avgdl, "df": df, "n_docs": len(docs)}


def bm25_score(query, doc_tokens, stats, k1=1.2, b=0.75):
    q = tokenize(query)
    tf = Counter(doc_tokens)
    dl = len(doc_tokens)
    avgdl = stats["avgdl"] or 1.0
    n = stats["n_docs"] or 1
    df = stats["df"]

    score = 0.0
    for term in q:
        f = tf.get(term, 0)
        if f == 0:
            continue
        # IDF with smoothing
        dfi = df.get(term, 0)
        idf = math.log(1.0 + (n - dfi + 0.5) / (dfi + 0.5))
        denom = f + k1 * (1.0 - b + b * (dl / avgdl))
        score += idf * (f * (k1 + 1.0)) / (denom if denom else 1.0)
    return score


def top_k(query, docs, k=3):
    stats = build_corpus_stats(docs)
    scored = []
    for i, toks in enumerate(stats["tokenized"]):
        scored.append((bm25_score(query, toks, stats), docs[i]))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]

