from collections import Counter


def build_vocab(docs, min_freq=1, max_features=None):
    """Build a vocabulary dict mapping token to index."""
    counter = Counter()
    for doc in docs:
        counter.update(doc)
    items = [item for item in counter.items() if item[1] >= min_freq]
    items.sort(key=lambda x: (-x[1], x[0]))
    if max_features is not None:
        items = items[:max_features]
    return {token: i for i, (token, _) in enumerate(items)}


def vectorize_bow(docs, vocab=None):
    """Convert documents to bag-of-words sparse vectors (dicts)."""
    if vocab is None:
        vocab = build_vocab(docs)
    vectors = []
    for doc in docs:
        counts = Counter(doc)
        vec = {vocab[t]: c for t, c in counts.items() if t in vocab}
        vectors.append(vec)
    return vectors, vocab


def term_frequency(counts):
    """Compute term frequency from a Counter or dict of counts."""
    total = sum(counts.values())
    if total == 0:
        return {k: 0.0 for k in counts}
    return {k: v / total for k, v in counts.items()}


def inverse_document_frequency(doc_counts, n_docs, smooth=True):
    """Compute inverse document frequency for term -> doc_count mapping."""
    idf = {}
    for term, dc in doc_counts.items():
        if smooth:
            idf[term] = 1.0 + (n_docs / (1.0 + dc))
        else:
            idf[term] = n_docs / max(dc, 1)
    return idf


def tfidf(docs, vocab=None):
    """Compute TF-IDF vectors for tokenized docs."""
    if vocab is None:
        vocab = build_vocab(docs)
    # document frequency
    doc_counts = {t: 0 for t in vocab}
    for doc in docs:
        seen = set(t for t in doc if t in vocab)
        for t in seen:
            doc_counts[t] += 1
    idf = inverse_document_frequency(doc_counts, len(docs), smooth=True)

    vectors = []
    for doc in docs:
        counts = Counter(doc)
        tf = term_frequency(counts)
        vec = {}
        for t, tfv in tf.items():
            if t in vocab:
                vec[vocab[t]] = tfv * idf[t]
        vectors.append(vec)
    return vectors, vocab
