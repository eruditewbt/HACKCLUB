from __future__ import annotations

from typing import Any, Dict, List, Optional

from dataanalysis_platform.core.timeutils import iso_utc_now
from dataanalysis_platform.io.files_csv import iter_csv_rows
from dataanalysis_platform.quality.rules import parse_rules


def _score(total_checks: int, failed_checks: int) -> float:
    if total_checks <= 0:
        return 1.0
    return max(0.0, (total_checks - failed_checks) / total_checks)


def validate_csv(path: str, rules_spec: Dict[str, Any], *, max_rows: Optional[int] = None) -> Dict:
    rules = parse_rules(rules_spec)

    failures: List[Dict[str, Any]] = []
    total_checks = 0
    failed_checks = 0

    row_count = 0
    for row in iter_csv_rows(path, max_rows=max_rows):
        row_count += 1
        for rule in rules:
            total_checks += 1
            ok, msg = rule.validate_row(row)
            if not ok:
                failed_checks += 1
                if len(failures) < 2000:
                    failures.append({
                        "row": row_count,
                        "rule": getattr(rule, "type", "rule"),
                        "message": msg,
                    })

    return {
        "kind": "validation",
        "source": {"path": path},
        "generated_at": iso_utc_now(),
        "row_count": row_count,
        "total_checks": total_checks,
        "failed_checks": failed_checks,
        "quality_score": _score(total_checks, failed_checks),
        "failures": failures,
        "rules": rules_spec,
    }

