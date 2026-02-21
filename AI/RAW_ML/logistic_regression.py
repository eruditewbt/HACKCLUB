import math


def _sigmoid(z):
    z = max(min(z, 35.0), -35.0)
    return 1.0 / (1.0 + math.exp(-z))


class LogisticRegressionGD:
    """Binary logistic regression with batch gradient descent."""

    def __init__(self, lr=0.1, epochs=1000, threshold=0.5):
        self.lr = lr
        self.epochs = epochs
        self.threshold = threshold
        self.weights = None
        self.bias = 0.0

    def fit(self, X, y):
        if not X:
            return self
        n_samples = len(X)
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            grad_w = [0.0] * n_features
            grad_b = 0.0
            for xi, yi in zip(X, y):
                pred = _sigmoid(sum(w * xj for w, xj in zip(self.weights, xi)) + self.bias)
                err = pred - yi
                for j in range(n_features):
                    grad_w[j] += err * xi[j]
                grad_b += err
            for j in range(n_features):
                self.weights[j] -= self.lr * (grad_w[j] / n_samples)
            self.bias -= self.lr * (grad_b / n_samples)
        return self

    def predict_proba(self, X):
        return [_sigmoid(sum(w * xj for w, xj in zip(self.weights, x)) + self.bias) for x in X]

    def predict(self, X):
        return [1 if p >= self.threshold else 0 for p in self.predict_proba(X)]
