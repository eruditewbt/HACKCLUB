from __future__ import annotations

from .logistic import Logistic2D, train_sgd


def main():
    # linearly separable toy set
    X = [(0.0, 0.0), (0.2, 0.1), (1.0, 1.0), (1.2, 0.9), (0.1, 0.3), (1.1, 1.3)]
    y = [0, 0, 1, 1, 0, 1]

    model = Logistic2D()
    train_sgd(model, X, y, lr=0.4, epochs=250)

    correct = 0
    for (x0, x1), yi in zip(X, y):
        pred = model.predict(x0, x1)
        correct += 1 if pred == yi else 0
    print("Training accuracy:", correct / len(X))
    print("Weights:", model)


if __name__ == "__main__":
    main()

