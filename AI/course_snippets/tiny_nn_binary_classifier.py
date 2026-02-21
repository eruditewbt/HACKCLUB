import math
import random


def sigmoid(x):
    x = max(min(x, 35.0), -35.0)
    return 1.0 / (1.0 + math.exp(-x))


class TinyNN:
    def __init__(self):
        self.w1 = random.uniform(-1.0, 1.0)
        self.w2 = random.uniform(-1.0, 1.0)
        self.b = 0.0

    def predict_prob(self, x1, x2):
        return sigmoid(self.w1 * x1 + self.w2 * x2 + self.b)

    def train_step(self, x1, x2, y, lr=0.1):
        p = self.predict_prob(x1, x2)
        grad = (p - y) * p * (1 - p)
        self.w1 -= lr * grad * x1
        self.w2 -= lr * grad * x2
        self.b -= lr * grad


def main():
    data = [
        (0.0, 0.0, 0),
        (0.0, 1.0, 1),
        (1.0, 0.0, 1),
        (1.0, 1.0, 1),
    ]
    nn = TinyNN()
    for _ in range(3000):
        x1, x2, y = random.choice(data)
        nn.train_step(x1, x2, y, lr=0.15)

    for x1, x2, y in data:
        p = nn.predict_prob(x1, x2)
        print((x1, x2), "p=", round(p, 4), "pred=", int(p >= 0.5), "y=", y)


if __name__ == "__main__":
    main()
