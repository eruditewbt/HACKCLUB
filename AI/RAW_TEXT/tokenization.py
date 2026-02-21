import re

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_WORD_RE = re.compile(r"[A-Za-z0-9']+")


def sentence_split(text):
    """Split text into sentences using simple punctuation rules."""
    text = text.strip()
    if not text:
        return []
    return _SENTENCE_RE.split(text)


def word_tokenize(text):
    """Tokenize text into word-like tokens."""
    return _WORD_RE.findall(text)


def ngrams(tokens, n):
    """Generate token n-grams from a list of tokens."""
    if n <= 0:
        return []
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def char_ngrams(text, n):
    """Generate character n-grams from text."""
    if n <= 0:
        return []
    return [text[i : i + n] for i in range(len(text) - n + 1)]
