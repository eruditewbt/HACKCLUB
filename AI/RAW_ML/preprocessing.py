import math


def minmax_scale(X):
    if not X:
        return X
    n_features = len(X[0])
    mins = [min(x[j] for x in X) for j in range(n_features)]
    maxs = [max(x[j] for x in X) for j in range(n_features)]
    scaled = []
    for x in X:
        row = []
        for j in range(n_features):
            denom = (maxs[j] - mins[j])
            row.append((x[j] - mins[j]) / denom if denom else 0.0)
        scaled.append(row)
    return scaled


def standardize(X):
    if not X:
        return X
    n_features = len(X[0])
    means = [sum(x[j] for x in X) / len(X) for j in range(n_features)]
    stds = []
    for j in range(n_features):
        var = sum((x[j] - means[j]) ** 2 for x in X) / len(X)
        stds.append(math.sqrt(var))
    scaled = []
    for x in X:
        row = []
        for j in range(n_features):
            row.append((x[j] - means[j]) / stds[j] if stds[j] else 0.0)
        scaled.append(row)
    return scaled


def normalize_l2(X):
    if not X:
        return X
    scaled = []
    for x in X:
        norm = math.sqrt(sum(v * v for v in x))
        if norm == 0.0:
            scaled.append(list(x))
        else:
            scaled.append([v / norm for v in x])
    return scaled


def one_hot(values):
    """One-hot encode a list of categorical values."""
    uniques = list(dict.fromkeys(values))
    index = {v: i for i, v in enumerate(uniques)}
    out = []
    for v in values:
        row = [0] * len(uniques)
        row[index[v]] = 1
        out.append(row)
    return out, uniques
