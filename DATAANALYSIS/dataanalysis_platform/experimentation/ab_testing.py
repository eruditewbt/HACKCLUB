from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ProportionTestResult:
    p1: float
    p2: float
    lift: float
    z: float
    p_value_approx: float


def _normal_cdf(x: float) -> float:
    # Approx via erf
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def ztest_proportions(
    *,
    successes_a: int,
    trials_a: int,
    successes_b: int,
    trials_b: int,
) -> ProportionTestResult:
    if trials_a <= 0 or trials_b <= 0:
        raise ValueError("Trials must be > 0")

    p1 = successes_a / trials_a
    p2 = successes_b / trials_b
    p_pool = (successes_a + successes_b) / (trials_a + trials_b)

    se = math.sqrt(p_pool * (1 - p_pool) * (1 / trials_a + 1 / trials_b))
    if se == 0:
        z = 0.0
    else:
        z = (p2 - p1) / se

    # Two-sided p-value
    p = 2 * (1 - _normal_cdf(abs(z)))
    lift = (p2 - p1) / p1 if p1 != 0 else float("inf")
    return ProportionTestResult(p1=p1, p2=p2, lift=lift, z=z, p_value_approx=p)
