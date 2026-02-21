import math


def levenshtein(a, b):
    """Compute Levenshtein edit distance between two strings."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            ins = curr[j - 1] + 1
            delete = prev[j] + 1
            replace = prev[j - 1] + (0 if ca == cb else 1)
            curr.append(min(ins, delete, replace))
        prev = curr
    return prev[-1]


def jaccard(a, b):
    """Jaccard similarity between two iterables."""
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def cosine_sparse(vec_a, vec_b):
    """Cosine similarity for sparse vectors (dicts)."""
    if not vec_a or not vec_b:
        return 0.0
    dot = 0.0
    for k, v in vec_a.items():
        if k in vec_b:
            dot += v * vec_b[k]
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
