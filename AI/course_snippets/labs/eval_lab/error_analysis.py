from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Example:
    text: str
    y_true: int
    y_pred: int


def false_positives(examples: List[Example]) -> List[Example]:
    return [e for e in examples if e.y_true == 0 and e.y_pred == 1]


def false_negatives(examples: List[Example]) -> List[Example]:
    return [e for e in examples if e.y_true == 1 and e.y_pred == 0]


