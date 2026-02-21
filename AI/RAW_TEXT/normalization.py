import re
import string
import unicodedata

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_unicode(text, form="NFKC"):
    """Normalize unicode text to a given form."""
    return unicodedata.normalize(form, text)


def strip_accents(text):
    """Remove accent marks from characters."""
    norm = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in norm if not unicodedata.combining(ch))


def to_ascii(text, replace=""):
    """Convert text to ASCII, optionally replacing non-ASCII chars."""
    norm = strip_accents(text)
    out = []
    for ch in norm:
        if ord(ch) < 128:
            out.append(ch)
        elif replace is not None:
            out.append(replace)
    return "".join(out)


def normalize_whitespace(text, strip=True):
    """Collapse whitespace runs into single spaces."""
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip() if strip else text


def remove_punctuation(text, keep_apostrophe=False):
    """Remove punctuation characters from text."""
    punct = string.punctuation
    if keep_apostrophe:
        punct = punct.replace("'", "")
    table = str.maketrans("", "", punct)
    return text.translate(table)


def remove_digits(text):
    """Remove digit characters from text."""
    return re.sub(r"\d+", "", text)


def clean_text(
    text,
    lower=True,
    remove_punct=True,
    remove_digit_chars=False,
    normalize_ws=True,
    strip=True,
):
    """Simple text cleaning pipeline with configurable steps."""
    if lower:
        text = text.lower()
    if remove_punct:
        text = remove_punctuation(text)
    if remove_digit_chars:
        text = remove_digits(text)
    if normalize_ws:
        text = normalize_whitespace(text, strip=strip)
    elif strip:
        text = text.strip()
    return text
