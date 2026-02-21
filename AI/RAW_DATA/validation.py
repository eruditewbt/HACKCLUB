import re

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
_URL_RE = re.compile(r"^(https?://)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_email(value):
    return bool(_EMAIL_RE.match(value or ""))


def is_url(value):
    return bool(_URL_RE.match(value or ""))


def is_int(value):
    try:
        int(value)
        return True
    except (TypeError, ValueError):
        return False


def is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def is_date(value):
    return bool(_DATE_RE.match(value or ""))


def ensure_required_keys(row, keys):
    return all(k in row and row[k] is not None for k in keys)
