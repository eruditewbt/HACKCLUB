from __future__ import annotations

import argparse
import json
import sys

from intel_planner import REQUIRED_KEYS, advanced_project_plan, prompt_to_pdss_input
from pdss_prob import ProjectDSS


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="PDSS Python planner (prompt -> plan JSON)")
    p.add_argument("--prompt", type=str, default="", help="Natural language project prompt")
    p.add_argument("--characteristics", type=str, default="", help="JSON string for project_characteristics (optional)")
    args = p.parse_args(argv)

    prompt = args.prompt or ""
    if args.characteristics:
        try:
            characteristics = json.loads(args.characteristics)
        except json.JSONDecodeError:
            print("Invalid --characteristics JSON", file=sys.stderr)
            return 2
        if not isinstance(characteristics, dict):
            print("--characteristics must be a JSON object", file=sys.stderr)
            return 2
    else:
        characteristics = prompt_to_pdss_input(prompt)

    missing = [k for k in REQUIRED_KEYS if k not in characteristics]
    if missing and prompt:
        inferred = prompt_to_pdss_input(prompt)
        for k in missing:
            characteristics[k] = inferred.get(k)
        missing = [k for k in REQUIRED_KEYS if k not in characteristics]
    if missing:
        print(json.dumps({"ok": False, "error": "Missing required keys", "missing": missing}, indent=2))
        return 2

    dss = ProjectDSS()
    dss.project_characteristics = characteristics
    dss.analyze_and_recommend()
    plan = advanced_project_plan(prompt, dss.project_characteristics, dss.recommendations)

    out = {
        "ok": True,
        "prompt": prompt,
        "project_characteristics": dss.project_characteristics,
        "recommendations": dss.recommendations,
        **plan,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

