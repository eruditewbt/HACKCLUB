import math


def _euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


class KNNClassifier:
    def __init__(self, k=3, distance="euclidean"):
        self.k = k
        self.distance = distance
        self.X = []
        self.y = []

    def fit(self, X, y):
        self.X = X
        self.y = y
        return self

    def _dist(self, a, b):
        if self.distance == "manhattan":
            return _manhattan(a, b)
        return _euclidean(a, b)

    def predict(self, X):
        preds = []
        for x in X:
            distances = [(self._dist(x, xi), yi) for xi, yi in zip(self.X, self.y)]
            distances.sort(key=lambda t: t[0])
            k_neigh = [label for _, label in distances[: self.k]]
            counts = {}
            for label in k_neigh:
                counts[label] = counts.get(label, 0) + 1
            preds.append(max(counts, key=counts.get))
        return preds


class KNNRegressor:
    def __init__(self, k=3, distance="euclidean"):
        self.k = k
        self.distance = distance
        self.X = []
        self.y = []

    def fit(self, X, y):
        self.X = X
        self.y = y
        return self

    def _dist(self, a, b):
        if self.distance == "manhattan":
            return _manhattan(a, b)
        return _euclidean(a, b)

    def predict(self, X):
        preds = []
        for x in X:
            distances = [(self._dist(x, xi), yi) for xi, yi in zip(self.X, self.y)]
            distances.sort(key=lambda t: t[0])
            k_neigh = [label for _, label in distances[: self.k]]
            preds.append(sum(k_neigh) / len(k_neigh) if k_neigh else 0.0)
        return preds
