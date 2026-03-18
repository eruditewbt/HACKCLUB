from __future__ import annotations

import argparse
import json
from typing import Any, Dict, Optional

from dataanalysis_platform.pipelines.orchestration import run_pipeline_csv


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--org-id", default="default")
    p.add_argument("--dataset", default="dataset")
    p.add_argument("--out", default="artifacts")
    p.add_argument("--max-rows", type=int, default=None)
    p.add_argument("--no-persist", action="store_true", help="Do not store runs in Postgres even if DATABASE_URL is set")
    p.add_argument("--webhook-url", default=None, help="Override webhook URL for alerts")


def main(argv: Any = None) -> int:
    p = argparse.ArgumentParser(prog="dataanalysis-platform")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_profile = sub.add_parser("profile", help="Profile only (no validation)")
    p_profile.add_argument("--input", required=True)
    _add_common(p_profile)

    p_validate = sub.add_parser("validate", help="Profile + validate + report")
    p_validate.add_argument("--input", required=True)
    p_validate.add_argument("--rules", required=True)
    _add_common(p_validate)

    p_run = sub.add_parser("run-all", help="Single command: profile + optional validation + report")
    p_run.add_argument("--input", required=True)
    p_run.add_argument("--rules", required=False)
    _add_common(p_run)

    args = p.parse_args(argv)

    persist = not args.no_persist

    if args.cmd == "profile":
        art = run_pipeline_csv(
            csv_path=args.input,
            rules_spec=None,
            artifacts_dir=args.out,
            max_rows=args.max_rows,
            org_id=args.org_id,
            dataset_name=args.dataset,
            webhook_url=args.webhook_url,
            persist=persist,
        )
        print(json.dumps({"run_id": art["run_id"], "artifact": art["artifact_path"]}, indent=2))
        return 0

    if args.cmd == "validate":
        rules = _load_json(args.rules)
        art = run_pipeline_csv(
            csv_path=args.input,
            rules_spec=rules,
            artifacts_dir=args.out,
            max_rows=args.max_rows,
            org_id=args.org_id,
            dataset_name=args.dataset,
            webhook_url=args.webhook_url,
            persist=persist,
        )
        print(
            json.dumps(
                {
                    "run_id": art["run_id"],
                    "artifact": art["artifact_path"],
                    "report_html": art.get("report_html"),
                },
                indent=2,
            )
        )
        return 0

    if args.cmd == "run-all":
        rules_spec: Optional[Dict[str, Any]] = None
        if args.rules:
            rules_spec = _load_json(args.rules)
        art = run_pipeline_csv(
            csv_path=args.input,
            rules_spec=rules_spec,
            artifacts_dir=args.out,
            max_rows=args.max_rows,
            org_id=args.org_id,
            dataset_name=args.dataset,
            webhook_url=args.webhook_url,
            persist=persist,
        )
        print(
            json.dumps(
                {
                    "run_id": art["run_id"],
                    "artifact": art["artifact_path"],
                    "report_html": art.get("report_html"),
                },
                indent=2,
            )
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
