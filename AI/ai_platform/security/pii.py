from __future__ import annotations

import re
from typing import Dict


_PATTERNS = {
    "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    "phone": re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}


def redact_pii(text: str) -> str:
    out = text
    out = _PATTERNS["email"].sub("[REDACTED_EMAIL]", out)
    out = _PATTERNS["phone"].sub("[REDACTED_PHONE]", out)
    out = _PATTERNS["ssn"].sub("[REDACTED_SSN]", out)
    return out


def pii_stats(text: str) -> Dict[str, int]:
    return {k: len(p.findall(text)) for k, p in _PATTERNS.items()}
