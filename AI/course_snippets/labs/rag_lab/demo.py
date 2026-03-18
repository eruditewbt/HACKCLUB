from __future__ import annotations

from .chunking import chunk_text
from .retrieval import build_index, score_tfidf


DOCS = {
    "doc1": "Python is a programming language. It is great for scripting, automation, and data science.",
    "doc2": "Netlify Functions run on Node.js. They are typically implemented in JavaScript or TypeScript.",
    "doc3": "Factor graphs represent joint distributions using factors. Belief propagation can compute marginals on trees.",
}


def main():
    chunks = []
    for doc_id, text in DOCS.items():
        chunks.extend(chunk_text(doc_id, text, chunk_size=120, overlap=20))
    index = build_index(chunks)

    print("Tiny RAG lab. Type a question; top chunks will be retrieved.\n")
    while True:
        q = input("Q (empty to quit): ").strip()
        if not q:
            break
        hits = score_tfidf(index, q, k=3)
        if not hits:
            print("No hits.\n")
            continue
        for score, ch in hits:
            print(f"- score={score:.3f} {ch.doc_id}#{ch.chunk_id}: {ch.text}")
        print()


if __name__ == "__main__":
    main()

