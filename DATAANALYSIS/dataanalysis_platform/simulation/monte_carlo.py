from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple


@dataclass(frozen=True)
class SimulationResult:
    n: int
    mean: float
    p05: float
    p50: float
    p95: float


def _percentile(sorted_vals: List[float], q: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = int(round((len(sorted_vals) - 1) * q))
    idx = max(0, min(len(sorted_vals) - 1, idx))
    return sorted_vals[idx]


def run_simulation(n: int, sampler: Callable[[random.Random], float], seed: int = 0) -> SimulationResult:
    rng = random.Random(seed)
    vals = [sampler(rng) for _ in range(n)]
    vals_sorted = sorted(vals)
    mean = sum(vals) / n if n else 0.0
    return SimulationResult(
        n=n,
        mean=mean,
        p05=_percentile(vals_sorted, 0.05),
        p50=_percentile(vals_sorted, 0.50),
        p95=_percentile(vals_sorted, 0.95),
    )
