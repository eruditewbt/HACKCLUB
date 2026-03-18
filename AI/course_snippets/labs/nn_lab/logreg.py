import math
import random


def sigmoid(x):
    x = max(min(x, 35.0), -35.0)
    return 1.0 / (1.0 + math.exp(-x))


class Logistic2D:
    def __init__(self, seed=None):
        rnd = random.Random(seed)
        self.w1 = rnd.uniform(-1.0, 1.0)
        self.w2 = rnd.uniform(-1.0, 1.0)
        self.b = 0.0

    def predict_prob(self, x1, x2):
        return sigmoid(self.w1 * x1 + self.w2 * x2 + self.b)

    def predict(self, x1, x2, threshold=0.5):
        return 1 if self.predict_prob(x1, x2) >= threshold else 0

    def train_step(self, x1, x2, y, lr=0.1):
        p = self.predict_prob(x1, x2)
        # logistic loss gradient (single sample)
        grad = (p - y)
        self.w1 -= lr * grad * x1
        self.w2 -= lr * grad * x2
        self.b -= lr * grad


