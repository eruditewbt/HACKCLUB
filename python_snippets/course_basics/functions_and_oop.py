from dataclasses import dataclass


def normalize(values):
    if not values:
        return []
    lo, hi = min(values), max(values)
    if lo == hi:
        return [0.0] * len(values)
    return [(v - lo) / (hi - lo) for v in values]


@dataclass
class Sample:
    features: list[float]
    label: int


samples = [Sample([2.0, 3.0], 1), Sample([0.0, 1.0], 0)]
print(normalize([10, 20, 30]))
print(samples)
