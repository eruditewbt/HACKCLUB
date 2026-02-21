# RAW_TEXT

Pure-Python text processing utilities with no third-party dependencies.

## Modules
- `normalization.py`: Unicode normalization, accent stripping, punctuation/digit removal, whitespace cleanup.
- `tokenization.py`: Sentence splitting, word tokenization, n-grams.
- `stopwords.py`: Small default stopword list + removal helper.
- `vectorize.py`: Bag-of-words and TF-IDF (sparse dict vectors).
- `similarity.py`: Levenshtein distance, Jaccard, cosine for sparse vectors.
- `keywords.py`: Keyword frequency and top-k extraction.

## Quick start
```python
from RAW_TEXT import clean_text, word_tokenize, tfidf

text = "Hello, world! This is a test."
clean = clean_text(text)

tokens = word_tokenize(clean)
print(tokens)

vectors, vocab = tfidf([tokens])
print(vectors, vocab)
```

## Notes
- Tokenization is regex-based and intentionally simple.
- TF-IDF vectors are sparse dicts keyed by vocab indices.
