from collections import Counter
from .tokenization import word_tokenize
from .stopwords import DEFAULT_STOPWORDS


def keyword_frequencies(text, stopwords=None, tokenizer=None):
    """Return token frequency map from text."""
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS
    if tokenizer is None:
        tokenizer = word_tokenize
    tokens = [t.lower() for t in tokenizer(text)]
    tokens = [t for t in tokens if t not in stopwords]
    return Counter(tokens)


def top_keywords(text, k=10, stopwords=None, tokenizer=None):
    """Return top-k keywords by frequency."""
    freq = keyword_frequencies(text, stopwords=stopwords, tokenizer=tokenizer)
    return freq.most_common(k)
