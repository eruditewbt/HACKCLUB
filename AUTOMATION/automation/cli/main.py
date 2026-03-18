from __future__ import annotations

import argparse
import json
import uuid

from automation.engine.config import load_settings
from automation.engine.runner import WorkflowRunner
from automation.engine.workflow import load_workflow
from automation.engine.state_store import FileStateStore
from automation.tasks import default_registry


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="automation")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run a workflow")
    p_run.add_argument("--workflow", required=True)
    p_run.add_argument("--org-id", default="default")
    p_run.add_argument("--run-id", default=None)

    p_status = sub.add_parser("status", help="Show run status")
    p_status.add_argument("--run", required=True)

    p_art = sub.add_parser("artifacts", help="Print artifacts folder for a run")
    p_art.add_argument("--run", required=True)

    p_sched = sub.add_parser("schedule", help="Run scheduler loop from a schedules file")
    p_sched.add_argument("--schedules", default="schedules.json", help="Path to schedules json")
    p_sched.add_argument("--poll-s", type=float, default=1.0)

    p_add = sub.add_parser("schedule-add", help="Add a schedule entry to a schedules file")
    p_add.add_argument("--schedules", default="schedules.json")
    p_add.add_argument("--workflow", required=True)
    p_add.add_argument("--org-id", default="default")
    p_add.add_argument("--cron", default=None)
    p_add.add_argument("--interval-s", type=int, default=None)

    args = p.parse_args(argv)
    settings = load_settings()

    if args.cmd == "run":
        run_id = args.run_id or uuid.uuid4().hex
        wf = load_workflow(args.workflow)
        runner = WorkflowRunner(registry=default_registry())
        summary = runner.run(
            wf=wf,
            run_id=run_id,
            org_id=args.org_id,
            artifacts_root=settings.artifacts_dir,
            state_root=settings.state_dir,
        )
        print(json.dumps({"run_id": summary.run_id, "ok": summary.ok, "artifacts_dir": f"{settings.artifacts_dir}/{summary.run_id}"}, indent=2))
        return 0 if summary.ok else 2

    if args.cmd == "status":
        st = FileStateStore(root_dir=settings.state_dir)
        data = st.read_run_summary(args.run)
        if data is None:
            print("Run not found")
            return 1
        print(json.dumps(data, indent=2))
        return 0

    if args.cmd == "artifacts":
        print(f"{settings.artifacts_dir}/{args.run}")
        return 0

    if args.cmd == "schedule-add":
        from automation.engine.scheduler import Schedule, load_schedules, save_schedules

        if not args.cron and not args.interval_s:
            print("Provide --cron or --interval-s")
            return 2

        schedules = load_schedules(args.schedules)
        sid = uuid.uuid4().hex
        schedules.append(
            Schedule(
                schedule_id=sid,
                workflow_path=args.workflow,
                org_id=args.org_id,
                cron=args.cron,
                interval_s=args.interval_s,
                enabled=True,
            )
        )
        save_schedules(args.schedules, schedules)
        print(json.dumps({"added": sid, "schedules": args.schedules}, indent=2))
        return 0

    if args.cmd == "schedule":
        from automation.engine.scheduler import InProcessScheduler

        sched = InProcessScheduler(
            runner=WorkflowRunner(registry=default_registry()),
            artifacts_root=settings.artifacts_dir,
            state_root=settings.state_dir,
        )
        sched.run_forever(schedules_path=args.schedules, poll_s=args.poll_s)
        return 0

    return 2
