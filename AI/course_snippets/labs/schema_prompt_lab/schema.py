from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class Field:
    name: str
    type_: type
    required: bool = True


def validate_object(obj: Any, fields: List[Field]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if not isinstance(obj, dict):
        return False, ["Expected a JSON object (dict)."]
    for f in fields:
        if f.required and f.name not in obj:
            errors.append(f"Missing required field: {f.name}")
            continue
        if f.name in obj and not isinstance(obj[f.name], f.type_):
            errors.append(f"Field {f.name} expected {f.type_.__name__}, got {type(obj[f.name]).__name__}")
    return len(errors) == 0, errors


