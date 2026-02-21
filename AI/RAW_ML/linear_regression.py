class LinearRegressionGD:
    """Simple linear regression with batch gradient descent."""

    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs
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
                pred = self._predict_row(xi)
                err = pred - yi
                for j in range(n_features):
                    grad_w[j] += err * xi[j]
                grad_b += err
            for j in range(n_features):
                self.weights[j] -= self.lr * (grad_w[j] / n_samples)
            self.bias -= self.lr * (grad_b / n_samples)
        return self

    def _predict_row(self, x):
        return sum(w * xj for w, xj in zip(self.weights, x)) + self.bias

    def predict(self, X):
        return [self._predict_row(x) for x in X]
