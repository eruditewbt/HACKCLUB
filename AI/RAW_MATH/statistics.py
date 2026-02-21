import math


def mean(values):
    return sum(values) / len(values) if values else 0.0


def median(values):
    if not values:
        return 0.0
    vals = sorted(values)
    n = len(vals)
    mid = n // 2
    if n % 2 == 1:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2


def mode(values):
    if not values:
        return None
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return max(counts, key=counts.get)


def variance(values, sample=False):
    if not values:
        return 0.0
    m = mean(values)
    denom = len(values) - 1 if sample and len(values) > 1 else len(values)
    return sum((v - m) ** 2 for v in values) / denom if denom else 0.0


def stddev(values, sample=False):
    return math.sqrt(variance(values, sample=sample))


def quantile(values, q):
    if not values:
        return 0.0
    vals = sorted(values)
    pos = (len(vals) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(vals) - 1)
    if lo == hi:
        return vals[lo]
    return vals[lo] + (vals[hi] - vals[lo]) * (pos - lo)


def zscores(values):
    m = mean(values)
    s = stddev(values)
    if s == 0.0:
        return [0.0 for _ in values]
    return [(v - m) / s for v in values]


def covariance(a, b, sample=False):
    if not a or not b:
        return 0.0
    ma = mean(a)
    mb = mean(b)
    denom = len(a) - 1 if sample and len(a) > 1 else len(a)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / denom if denom else 0.0


def correlation(a, b):
    denom = stddev(a) * stddev(b)
    if denom == 0.0:
        return 0.0
    return covariance(a, b) / denom
