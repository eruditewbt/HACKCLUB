class Dataset:
    """Lightweight dataset wrapper around list of dict rows."""

    def __init__(self, rows):
        self.rows = list(rows)

    def head(self, n=5):
        return self.rows[:n]

    def select(self, keys):
        return Dataset([{k: row.get(k) for k in keys} for row in self.rows])

    def filter(self, predicate):
        return Dataset([row for row in self.rows if predicate(row)])

    def describe(self):
        """Basic count and nulls per key."""
        if not self.rows:
            return {}
        keys = set().union(*(row.keys() for row in self.rows))
        out = {}
        for k in keys:
            values = [row.get(k) for row in self.rows]
            nulls = sum(1 for v in values if v is None or v == "")
            out[k] = {"count": len(values), "nulls": nulls}
        return out
