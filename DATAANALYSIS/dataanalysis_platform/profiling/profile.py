from __future__ import annotations

from typing import Dict, Optional

from dataanalysis_platform.core.timeutils import iso_utc_now
from dataanalysis_platform.io.files_csv import iter_csv_rows
from dataanalysis_platform.profiling.column_stats import ColumnStats
from dataanalysis_platform.profiling.schema_infer import infer_type


def profile_csv(path: str, *, max_rows: Optional[int] = None) -> Dict:
    head = []
    for i, row in enumerate(iter_csv_rows(path, max_rows=500)):
        head.append(row)
        if i >= 499:
            break

    if not head:
        return {
            "kind": "profile",
            "source": {"path": path},
            "generated_at": iso_utc_now(),
            "row_count": 0,
            "columns": [],
        }

    columns = list(head[0].keys())

    inferred = {}
    for c in columns:
        values = [r.get(c, "") for r in head]
        inferred[c] = infer_type(values).name

    stats = {c: ColumnStats(name=c, inferred_type=inferred[c]) for c in columns}

    row_count = 0
    for row in iter_csv_rows(path, max_rows=max_rows):
        row_count += 1
        for c in columns:
            stats[c].update(row.get(c, ""))

    return {
        "kind": "profile",
        "source": {"path": path},
        "generated_at": iso_utc_now(),
        "row_count": row_count,
        "columns": [stats[c].as_dict() for c in columns],
    }

