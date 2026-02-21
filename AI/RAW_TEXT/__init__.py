"""Raw text processing utilities (no third-party dependencies)."""
from .normalization import (
    normalize_unicode,
    strip_accents,
    to_ascii,
    normalize_whitespace,
    remove_punctuation,
    remove_digits,
    clean_text,
)
from .tokenization import (
    sentence_split,
    word_tokenize,
    ngrams,
    char_ngrams,
)
from .stopwords import DEFAULT_STOPWORDS, remove_stopwords
from .vectorize import (
    build_vocab,
    vectorize_bow,
    term_frequency,
    inverse_document_frequency,
    tfidf,
)
from .similarity import levenshtein, jaccard, cosine_sparse
from .keywords import keyword_frequencies, top_keywords
