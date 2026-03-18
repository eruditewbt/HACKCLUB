from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DriftFinding:
    column: str
    kind: str
    previous: Any
    current: Any
    severity: str


def _index_by_name(profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    cols = profile.get("columns") or []
    return {str(c.get("name")): c for c in cols}


def detect_drift(
    *,
    previous_profile: Dict[str, Any],
    current_profile: Dict[str, Any],
    missing_rate_delta: float = 0.10,
    mean_std_delta: float = 3.0,
) -> List[Dict[str, Any]]:
    """Heuristic drift detection using stored profile stats.

    Monetizable direction: reliability monitoring + alerting.
    """

    prev = _index_by_name(previous_profile)
    cur = _index_by_name(current_profile)

    findings: List[DriftFinding] = []

    for col, cnow in cur.items():
        cold = prev.get(col)
        if not cold:
            findings.append(DriftFinding(column=col, kind="new_column", previous=None, current=True, severity="info"))
            continue

        mr_old = float(cold.get("missing_rate") or 0.0)
        mr_new = float(cnow.get("missing_rate") or 0.0)
        if abs(mr_new - mr_old) >= missing_rate_delta:
            severity = "high" if abs(mr_new - mr_old) >= (2 * missing_rate_delta) else "medium"
            findings.append(
                DriftFinding(
                    column=col,
                    kind="missing_rate",
                    previous=mr_old,
                    current=mr_new,
                    severity=severity,
                )
            )

        t = str(cnow.get("type") or "string")
        if t in {"int", "float"}:
            mean_old = cold.get("mean")
            mean_new = cnow.get("mean")
            std_old = float(cold.get("std") or 0.0)
            if mean_old is not None and mean_new is not None and std_old > 0:
                delta_std = abs(float(mean_new) - float(mean_old)) / std_old
                if delta_std >= mean_std_delta:
                    severity = "high" if delta_std >= (2 * mean_std_delta) else "medium"
                    findings.append(
                        DriftFinding(
                            column=col,
                            kind="mean_shift",
                            previous={"mean": mean_old, "std": std_old},
                            current={"mean": mean_new, "std": cnow.get("std")},
                            severity=severity,
                        )
                    )

    for col in prev.keys():
        if col not in cur:
            findings.append(DriftFinding(column=col, kind="missing_column", previous=True, current=None, severity="high"))

    return [
        {
            "column": f.column,
            "kind": f.kind,
            "previous": f.previous,
            "current": f.current,
            "severity": f.severity,
        }
        for f in findings
    ]
