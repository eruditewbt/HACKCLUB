from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


class Rule:
    type: str

    def validate_row(self, row: Dict[str, str]) -> Tuple[bool, str]:
        raise NotImplementedError


@dataclass(frozen=True)
class NotNull(Rule):
    column: str
    type: str = "not_null"

    def validate_row(self, row: Dict[str, str]) -> Tuple[bool, str]:
        v = (row.get(self.column) or "").strip()
        ok = v != ""
        return ok, f"{self.column} must be non-empty"


@dataclass(frozen=True)
class RangeRule(Rule):
    column: str
    min: Optional[float] = None
    max: Optional[float] = None
    type: str = "range"

    def validate_row(self, row: Dict[str, str]) -> Tuple[bool, str]:
        raw = (row.get(self.column) or "").strip()
        if raw == "":
            return True, ""  # Let NotNull enforce presence.
        try:
            v = float(raw)
        except Exception:
            return False, f"{self.column} must be numeric"
        if self.min is not None and v < self.min:
            return False, f"{self.column} must be >= {self.min}"
        if self.max is not None and v > self.max:
            return False, f"{self.column} must be <= {self.max}"
        return True, ""


@dataclass(frozen=True)
class AllowedValues(Rule):
    column: str
    values: List[str]
    type: str = "allowed_values"

    def validate_row(self, row: Dict[str, str]) -> Tuple[bool, str]:
        raw = (row.get(self.column) or "").strip()
        if raw == "":
            return True, ""
        ok = raw in set(self.values)
        return ok, f"{self.column} must be one of {self.values}"


@dataclass(frozen=True)
class RegexMatch(Rule):
    column: str
    pattern: str
    type: str = "regex"

    def validate_row(self, row: Dict[str, str]) -> Tuple[bool, str]:
        raw = (row.get(self.column) or "").strip()
        if raw == "":
            return True, ""
        ok = re.search(self.pattern, raw) is not None
        return ok, f"{self.column} must match regex {self.pattern}"


def parse_rules(spec: Dict[str, Any]) -> List[Rule]:
    rules: List[Rule] = []
    for r in spec.get("rules", []):
        rtype = r.get("type")
        if rtype == "not_null":
            rules.append(NotNull(column=r["column"]))
        elif rtype == "range":
            rules.append(RangeRule(column=r["column"], min=r.get("min"), max=r.get("max")))
        elif rtype == "allowed_values":
            rules.append(AllowedValues(column=r["column"], values=list(r.get("values", []))))
        elif rtype == "regex":
            rules.append(RegexMatch(column=r["column"], pattern=r["pattern"]))
        else:
            raise ValueError(f"Unknown rule type: {rtype}")
    return rules
