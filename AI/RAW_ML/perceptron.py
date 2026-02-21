class Perceptron:
    """Simple binary perceptron."""

    def __init__(self, lr=0.1, epochs=10):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0

    def fit(self, X, y):
        if not X:
            return self
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                pred = self._predict_row(xi)
                update = self.lr * (yi - pred)
                for j in range(n_features):
                    self.weights[j] += update * xi[j]
                self.bias += update
        return self

    def _predict_row(self, x):
        score = sum(w * xj for w, xj in zip(self.weights, x)) + self.bias
        return 1 if score >= 0.0 else 0

    def predict(self, X):
        return [self._predict_row(x) for x in X]
