from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class ZScoreAnomaly:
    index: int
    value: float
    z: float


def zscore_anomalies(values: List[float], *, threshold: float = 3.0) -> List[ZScoreAnomaly]:
    if not values:
        return []
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    std = var ** 0.5
    if std == 0:
        return []

    out: List[ZScoreAnomaly] = []
    for i, v in enumerate(values):
        z = (v - mean) / std
        if abs(z) >= threshold:
            out.append(ZScoreAnomaly(index=i, value=v, z=z))
    return out
