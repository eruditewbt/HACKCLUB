from __future__ import annotations

import fnmatch
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple

from automation.engine.workflow import load_workflow
from automation.engine.runner import WorkflowRunner


def iso_utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@dataclass(frozen=True)
class FsWatchTrigger:
    """Poll-based filesystem watcher (stdlib-only).

    Triggers a workflow when a matching file is created/modified.
    """

    path: str
    pattern: str = "*"
    recursive: bool = True
    min_mtime_delta_s: float = 0.0


def _iter_files(base: str, recursive: bool) -> Iterable[str]:
    if recursive:
        for root, _, files in os.walk(base):
            for f in files:
                yield os.path.join(root, f)
    else:
        for f in os.listdir(base):
            p = os.path.join(base, f)
            if os.path.isfile(p):
                yield p


def watch_files(
    *,
    trigger: FsWatchTrigger,
    runner: WorkflowRunner,
    workflow_path: str,
    org_id: str,
    artifacts_root: str,
    state_root: str,
    poll_s: float = 1.0,
) -> None:
    last: Dict[str, float] = {}

    while True:
        if os.path.isdir(trigger.path):
            for p in _iter_files(trigger.path, trigger.recursive):
                name = os.path.basename(p)
                if not fnmatch.fnmatch(name, trigger.pattern):
                    continue
                try:
                    m = os.path.getmtime(p)
                except Exception:
                    continue
                prev = last.get(p)
                if prev is None or (m - prev) > trigger.min_mtime_delta_s:
                    last[p] = m
                    wf = load_workflow(workflow_path)
                    run_id = uuid.uuid4().hex
                    runner.run(
                        wf=wf,
                        run_id=run_id,
                        org_id=org_id,
                        artifacts_root=artifacts_root,
                        state_root=state_root,
                    )
        time.sleep(poll_s)

