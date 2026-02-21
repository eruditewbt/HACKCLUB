import math
from collections import Counter, defaultdict


class MultinomialNB:
    """Multinomial Naive Bayes for tokenized text."""

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.class_counts = Counter()
        self.token_counts = defaultdict(Counter)
        self.vocab = set()

    def fit(self, docs, labels):
        for doc, label in zip(docs, labels):
            self.class_counts[label] += 1
            counts = Counter(doc)
            self.token_counts[label].update(counts)
            self.vocab.update(counts.keys())
        return self

    def _log_prob(self, doc, label):
        total_tokens = sum(self.token_counts[label].values())
        vocab_size = len(self.vocab)
        log_prob = math.log(self.class_counts[label] / sum(self.class_counts.values()))
        counts = Counter(doc)
        for token, cnt in counts.items():
            num = self.token_counts[label][token] + self.alpha
            den = total_tokens + self.alpha * vocab_size
            log_prob += cnt * math.log(num / den)
        return log_prob

    def predict(self, docs):
        labels = list(self.class_counts.keys())
        preds = []
        for doc in docs:
            scores = {label: self._log_prob(doc, label) for label in labels}
            preds.append(max(scores, key=scores.get))
        return preds

    def predict_proba(self, docs):
        labels = list(self.class_counts.keys())
        out = []
        for doc in docs:
            scores = {label: self._log_prob(doc, label) for label in labels}
            max_score = max(scores.values())
            exp_scores = {l: math.exp(s - max_score) for l, s in scores.items()}
            total = sum(exp_scores.values())
            out.append({l: exp_scores[l] / total for l in labels})
        return out
