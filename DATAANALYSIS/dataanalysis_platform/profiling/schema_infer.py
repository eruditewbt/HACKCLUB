from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional


@dataclass(frozen=True)
class InferredType:
    name: str  # int, float, bool, date, datetime, string


def _try_int(s: str) -> bool:
    try:
        int(s)
        return True
    except Exception:
        return False


def _try_float(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False


def _try_bool(s: str) -> bool:
    v = s.strip().lower()
    return v in {"true", "false", "0", "1", "yes", "no"}


def _try_datetime(s: str) -> Optional[str]:
    v = s.strip()
    try:
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        if "T" in v or ":" in v:
            return "datetime"
        return "date"
    except Exception:
        return None


def infer_type(values: Iterable[str], *, sample_size: int = 200) -> InferredType:
    seen = 0
    non_empty = []
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if s == "":
            continue
        non_empty.append(s)
        seen += 1
        if seen >= sample_size:
            break

    if not non_empty:
        return InferredType("string")

    if all(_try_bool(x) for x in non_empty):
        return InferredType("bool")

    dt_kinds = [_try_datetime(x) for x in non_empty]
    if all(k is not None for k in dt_kinds):
        if any(k == "datetime" for k in dt_kinds):
            return InferredType("datetime")
        return InferredType("date")

    if all(_try_int(x) for x in non_empty):
        return InferredType("int")

    if all(_try_float(x) for x in non_empty):
        return InferredType("float")

    return InferredType("string")
