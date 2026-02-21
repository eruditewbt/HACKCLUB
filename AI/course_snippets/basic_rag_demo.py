from collections import Counter


def tokenize(text):
    return [t.strip(".,!?;:\"'()[]{}").lower() for t in text.split() if t.strip()]


def score(query, doc):
    q = Counter(tokenize(query))
    d = Counter(tokenize(doc))
    return sum(q[w] * d[w] for w in q)


def retrieve(query, docs, k=2):
    ranked = sorted(docs, key=lambda d: score(query, d), reverse=True)
    return ranked[:k]


def main():
    docs = [
        "Linear regression predicts continuous values.",
        "Logistic regression predicts probabilities for classes.",
        "A star search uses heuristics to guide exploration.",
    ]
    query = "How do we predict class probability"
    context = retrieve(query, docs)
    print("query:", query)
    print("context:")
    for c in context:
        print("-", c)


if __name__ == "__main__":
    main()
