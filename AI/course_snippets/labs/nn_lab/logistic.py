from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Tuple


def sigmoid(z: float) -> float:
    z = max(min(z, 35.0), -35.0)
    return 1.0 / (1.0 + math.exp(-z))


@dataclass
class Logistic2D:
    w0: float = 0.0
    w1: float = 0.0
    b: float = 0.0

    def predict_proba(self, x0: float, x1: float) -> float:
        return sigmoid(self.w0 * x0 + self.w1 * x1 + self.b)

    def predict(self, x0: float, x1: float) -> int:
        return 1 if self.predict_proba(x0, x1) >= 0.5 else 0


def train_sgd(
    model: Logistic2D,
    X: List[Tuple[float, float]],
    y: List[int],
    lr: float = 0.1,
    epochs: int = 200,
    seed: int = 0,
) -> Logistic2D:
    rng = random.Random(seed)
    for _ in range(epochs):
        idx = list(range(len(X)))
        rng.shuffle(idx)
        for i in idx:
            x0, x1 = X[i]
            yi = y[i]
            p = model.predict_proba(x0, x1)
            grad = (p - yi)
            model.w0 -= lr * grad * x0
            model.w1 -= lr * grad * x1
            model.b -= lr * grad
    return model


