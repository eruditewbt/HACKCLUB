from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ColumnStats:
    name: str
    inferred_type: str
    count: int = 0
    missing: int = 0
    distinct: set = field(default_factory=set)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    sum_value: float = 0.0
    sumsq_value: float = 0.0
    non_numeric: int = 0

    def update(self, raw: str) -> None:
        self.count += 1

        if raw is None:
            self.missing += 1
            return

        s = str(raw).strip()
        if s == "":
            self.missing += 1
            return

        if len(self.distinct) < 50_000:
            self.distinct.add(s)

        if self.inferred_type in {"int", "float"}:
            try:
                v = float(s)
            except Exception:
                self.non_numeric += 1
                return

            if self.min_value is None or v < self.min_value:
                self.min_value = v
            if self.max_value is None or v > self.max_value:
                self.max_value = v
            self.sum_value += v
            self.sumsq_value += v * v

    def as_dict(self) -> Dict:
        n_non_missing = self.count - self.missing
        mean = None
        std = None
        if self.inferred_type in {"int", "float"} and n_non_missing > 0:
            mean = self.sum_value / n_non_missing
            var = max(0.0, (self.sumsq_value / n_non_missing) - (mean * mean))
            std = var ** 0.5

        return {
            "name": self.name,
            "type": self.inferred_type,
            "count": self.count,
            "missing": self.missing,
            "missing_rate": (self.missing / self.count) if self.count else 0.0,
            "distinct_count": len(self.distinct),
            "min": self.min_value,
            "max": self.max_value,
            "mean": mean,
            "std": std,
            "non_numeric": self.non_numeric,
        }
