# RAG Lab (No Dependencies)

Goal: turn `basic_rag_demo.py` into a more realistic retrieval component you can reuse.

## Files
- `text.py`: tokenization + normalization helpers
- `bm25.py`: BM25-ish scoring (good baseline retrieval without embeddings)
- `chunking.py`: split documents into overlapping chunks
- `demo.py`: runnable example

## Run
```bash
python -m course_snippets.labs.rag_lab.demo
```

## Exercises
1. Add stopword removal and compare retrieval results.
2. Add phrase boosting (exact phrase match bonus).
3. Add a `--k` CLI arg for top-k results.
