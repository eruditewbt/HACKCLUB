from __future__ import annotations

import json
import os
import uuid
from typing import Any, Dict, Optional

from dataanalysis_platform.alerts.dispatcher import dispatch_validation_alert
from dataanalysis_platform.artifacts.db import make_engine
from dataanalysis_platform.core.timeutils import iso_utc_now
from dataanalysis_platform.profiling.profile import profile_csv
from dataanalysis_platform.quality.validators import validate_csv
from dataanalysis_platform.viz.report_html import render_report


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def run_pipeline_csv(
    *,
    csv_path: str,
    rules_spec: Optional[Dict[str, Any]] = None,
    artifacts_dir: str = "artifacts",
    max_rows: Optional[int] = None,
    title: str = "DATAANALYSIS Quality Report",
    org_id: str = "default",
    dataset_name: str = "dataset",
    webhook_url: Optional[str] = None,
    persist: bool = True,
) -> Dict[str, Any]:
    """Run the sellable vertical slice.

    - Profiles the dataset
    - Validates rules (optional)
    - Produces HTML report (when rules are provided)
    - Writes file artifacts
    - Persists to Postgres (if SQLAlchemy is installed and DATABASE_URL is set)
    - Sends webhook alerts (best-effort)
    """

    ensure_dir(artifacts_dir)

    run_id = uuid.uuid4().hex

    profile = profile_csv(csv_path, max_rows=max_rows)

    validation = None
    report_html_doc = None
    report_html_path = None

    if rules_spec is not None:
        validation = validate_csv(csv_path, rules_spec, max_rows=max_rows)

    artifact: Dict[str, Any] = {
        "kind": "artifact",
        "run_id": run_id,
        "generated_at": iso_utc_now(),
        "title": title,
        "org_id": org_id,
        "dataset_name": dataset_name,
        "source": {"path": csv_path},
        "profile": profile,
        "validation": validation,
    }

    artifact_path = os.path.join(artifacts_dir, f"{run_id}.json")
    with open(artifact_path, "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, ensure_ascii=True)

    latest_path = os.path.join(artifacts_dir, "latest.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump({"run_id": run_id, "artifact": artifact_path}, f, indent=2, ensure_ascii=True)

    if validation is not None:
        report_html_doc = render_report(artifact)
        report_html_path = os.path.join(artifacts_dir, f"{run_id}.html")
        with open(report_html_path, "w", encoding="utf-8") as f:
            f.write(report_html_doc)
        artifact["report_html"] = report_html_path

        failed_checks = int(validation.get("failed_checks") or 0)
        total_checks = int(validation.get("total_checks") or 0)
        if failed_checks > 0:
            dispatch_validation_alert(
                webhook_url=webhook_url,
                event={
                    "event": "data_validation_failed",
                    "org_id": org_id,
                    "dataset_name": dataset_name,
                    "run_id": run_id,
                    "failed_checks": failed_checks,
                    "total_checks": total_checks,
                    "quality_score": float(validation.get("quality_score") or 0.0),
                },
            )

    artifact["artifact_path"] = artifact_path

    if persist:
        engine = make_engine()
        if engine is not None:
            try:
                from dataanalysis_platform.artifacts.repository import init_db, save_run

                init_db(engine)
                save_run(
                    engine=engine,
                    run_id=run_id,
                    org_id=org_id,
                    dataset_name=dataset_name,
                    profile=profile,
                    validation=validation,
                    report_html=report_html_doc,
                )
            except Exception:
                # Persistence must not crash the pipeline.
                pass

    return artifact
