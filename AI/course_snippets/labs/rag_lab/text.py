import re


_WORD_RE = re.compile(r"[A-Za-z0-9']+")


def normalize(text):
    return (text or "").strip().lower()


def tokenize(text):
    return _WORD_RE.findall(normalize(text))


