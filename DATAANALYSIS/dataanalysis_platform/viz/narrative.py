from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


def _fmt_pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def _top_missing(cols: List[Dict[str, Any]], *, min_rate: float = 0.0, limit: int = 5):
    missing = []
    for c in cols:
        mr = float(c.get("missing_rate") or 0.0)
        if mr > min_rate:
            missing.append((mr, str(c.get("name"))))
    missing.sort(reverse=True)
    return missing[:limit]


def analyze_artifact(artifact: Dict[str, Any]) -> Dict[str, Any]:
    """Produce premium-looking narrative sections.

    Deterministic and context-driven: no static boilerplate blocks.
    """

    profile = artifact.get("profile") or {}
    validation = artifact.get("validation") or {}

    row_count = int(profile.get("row_count") or 0)
    cols = profile.get("columns") or []

    key_issues: List[str] = []
    recs: List[str] = []
    notes: List[str] = []

    if row_count == 0:
        return {
            "executive_summary": "No rows were detected. Confirm the CSV has a header row and at least one data row.",
            "key_issues": ["Empty dataset"],
            "recommendations": ["Verify the upstream export step and CSV formatting."],
            "notes": [],
        }

    # Validation score
    score = None
    failed = None
    total = None
    if validation:
        failed = int(validation.get("failed_checks") or 0)
        total = int(validation.get("total_checks") or 0)
        score = float(validation.get("quality_score") or 0.0)

    # Missingness
    top_missing_any = _top_missing(cols, min_rate=0.0)
    top_missing_high = _top_missing(cols, min_rate=0.20)

    if top_missing_high:
        key_issues.append(
            "High missingness detected in: "
            + ", ".join([f"{name} ({_fmt_pct(mr)} missing)" for mr, name in top_missing_high])
        )
        recs.append(
            "Treat high-missing columns as contract-breaking or define explicit imputation/" 
            "fallback rules so KPIs don’t silently drift when data is absent."
        )

    # Numeric quality hints
    numeric_with_non_numeric = []
    for c in cols:
        t = str(c.get("type") or "string")
        if t in {"int", "float"} and int(c.get("non_numeric") or 0) > 0:
            numeric_with_non_numeric.append((str(c.get("name")), int(c.get("non_numeric") or 0)))

    if numeric_with_non_numeric:
        key_issues.append(
            "Numeric parse issues in: " + ", ".join([f"{n} ({k} bad values)" for n, k in numeric_with_non_numeric[:5]])
        )
        recs.append(
            "Normalize numeric formatting upstream (thousands separators, currency symbols) "
            "or add a cleaning step before validation to avoid mixing strings into numeric columns."
        )

    # Validation failures pattern
    if validation and (validation.get("failures") or []):
        failures = validation.get("failures") or []
        by_rule = Counter([f.get("rule") for f in failures]).most_common(3)
        key_issues.append(
            "Top failing rule types: " + ", ".join([f"{r} ({n})" for r, n in by_rule])
        )

        # Tailored recommendations by rule-type
        rule_types = {r for r, _ in by_rule}
        if "allowed_values" in rule_types:
            recs.append(
                "For categorical constraints, introduce a reference table (or enum) and a normalization step "
                "(trim/case-fold) so reporting categories stay consistent."
            )
        if "range" in rule_types:
            recs.append(
                "For range failures, add upstream guards (e.g., database constraints) and investigate source-system "
                "unit changes (cents vs dollars) that often cause sudden out-of-range values."
            )
        if "not_null" in rule_types:
            recs.append(
                "For null failures, decide whether the field is truly required. If yes, make it mandatory upstream; "
                "if no, adjust the contract and update metrics to handle nulls explicitly."
            )

    # Executive summary
    parts = [f"Profiled {row_count} rows across {len(cols)} columns."]
    if score is not None and total is not None and failed is not None:
        parts.append(
            f"Validation executed {total} checks with {failed} failures (quality score: {score:.3f})."
        )
    if top_missing_any:
        parts.append(
            "Most missingness appears in: " + ", ".join([f"{name} ({_fmt_pct(mr)})" for mr, name in top_missing_any[:3]]) + "."
        )

    if not key_issues:
        key_issues.append("No high-severity issues detected in the scanned rows.")
        recs.append(
            "Keep this dataset stable by versioning the data contract and running validations on a schedule (daily/weekly) "
            "with alerts routed to your ops channel."
        )

    notes.append(
        "This report is deterministic and based on current profiling + contract results. "
        "As you store run history in Postgres, you can add drift detection and alerting for operational monitoring."
    )

    return {
        "executive_summary": " ".join(parts),
        "key_issues": key_issues,
        "recommendations": recs,
        "notes": notes,
    }
