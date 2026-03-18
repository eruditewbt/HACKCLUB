from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 1
    base_delay_s: float = 0.5
    max_delay_s: float = 10.0

    def delay_for_attempt(self, attempt: int) -> float:
        d = self.base_delay_s * (2 ** max(0, attempt - 1))
        return min(self.max_delay_s, d)


def run_with_retries(fn: Callable[[], T], policy: RetryPolicy) -> T:
    last_err = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt >= policy.max_attempts:
                raise
            time.sleep(policy.delay_for_attempt(attempt))
    raise last_err  # type: ignore[misc]
