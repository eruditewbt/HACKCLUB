from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from automation.engine.workflow import load_workflow
from automation.engine.runner import WorkflowRunner


def iso_utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _parse_int_set(token: str, min_v: int, max_v: int) -> Optional[set[int]]:
    """Parse a single cron field into a set of ints, or None for '*'."""
    token = token.strip()
    if token == "*":
        return None

    out: set[int] = set()
    parts = token.split(",")
    for p in parts:
        p = p.strip()
        if p.startswith("*/"):
            step = int(p[2:])
            for v in range(min_v, max_v + 1, step):
                out.add(v)
        elif "-" in p:
            a, b = p.split("-", 1)
            a_i = int(a)
            b_i = int(b)
            for v in range(a_i, b_i + 1):
                out.add(v)
        else:
            out.add(int(p))

    for v in out:
        if v < min_v or v > max_v:
            raise ValueError(f"Cron value out of range: {v} not in [{min_v},{max_v}]")
    return out


@dataclass(frozen=True)
class CronSpec:
    minutes: Optional[set[int]]
    hours: Optional[set[int]]
    dom: Optional[set[int]]
    month: Optional[set[int]]
    dow: Optional[set[int]]

    @staticmethod
    def parse(expr: str) -> "CronSpec":
        fields = [x for x in expr.strip().split() if x]
        if len(fields) != 5:
            raise ValueError("Cron must have 5 fields: min hour dom month dow")

        minute, hour, dom, month, dow = fields
        return CronSpec(
            minutes=_parse_int_set(minute, 0, 59),
            hours=_parse_int_set(hour, 0, 23),
            dom=_parse_int_set(dom, 1, 31),
            month=_parse_int_set(month, 1, 12),
            dow=_parse_int_set(dow, 0, 6),  # 0=Sunday .. 6=Saturday
        )

    def matches(self, dt: datetime) -> bool:
        if dt.tzinfo is None:
            raise ValueError("dt must be timezone-aware")
        # Python: Monday=0..Sunday=6. Cron often uses Sunday=0.
        cron_dow = (dt.weekday() + 1) % 7
        return all(
            [
                (self.minutes is None or dt.minute in self.minutes),
                (self.hours is None or dt.hour in self.hours),
                (self.dom is None or dt.day in self.dom),
                (self.month is None or dt.month in self.month),
                (self.dow is None or cron_dow in self.dow),
            ]
        )


def next_fire_time(cron: CronSpec, *, start: datetime, max_search_minutes: int = 60 * 24 * 366) -> datetime:
    """Find next dt >= start (minute resolution) where cron matches."""
    if start.tzinfo is None:
        raise ValueError("start must be timezone-aware")

    dt = start.replace(second=0, microsecond=0)
    for _ in range(max_search_minutes):
        if cron.matches(dt):
            return dt
        dt = dt + timedelta(minutes=1)
    raise RuntimeError("Cron search exceeded limit")


@dataclass
class Schedule:
    schedule_id: str
    workflow_path: str
    org_id: str
    cron: Optional[str] = None
    interval_s: Optional[int] = None
    enabled: bool = True
    last_run_at: Optional[str] = None
    next_run_at: Optional[str] = None


def load_schedules(path: str) -> List[Schedule]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for s in data.get("schedules", []):
        out.append(Schedule(**s))
    return out


def save_schedules(path: str, schedules: List[Schedule]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"schedules": [s.__dict__ for s in schedules]}, f, indent=2, ensure_ascii=True)


class InProcessScheduler:
    """Simple scheduler loop: cron or interval. File-based schedules."""

    def __init__(self, *, runner: WorkflowRunner, artifacts_root: str, state_root: str) -> None:
        self.runner = runner
        self.artifacts_root = artifacts_root
        self.state_root = state_root

    def compute_next(self, s: Schedule, now: datetime) -> Optional[datetime]:
        if not s.enabled:
            return None
        if s.cron:
            cron = CronSpec.parse(s.cron)
            # Start from next minute to avoid re-firing in the same minute.
            start = now + timedelta(minutes=1)
            return next_fire_time(cron, start=start)
        if s.interval_s:
            base = now
            if s.last_run_at:
                try:
                    base = datetime.fromisoformat(s.last_run_at)
                    if base.tzinfo is None:
                        base = base.replace(tzinfo=timezone.utc)
                except Exception:
                    base = now
            return base + timedelta(seconds=int(s.interval_s))
        return None

    def tick(self, schedules: List[Schedule], *, now: Optional[datetime] = None) -> List[Tuple[Schedule, str]]:
        now = now or datetime.now(tz=timezone.utc)
        fired: List[Tuple[Schedule, str]] = []

        for s in schedules:
            if not s.enabled:
                continue

            if s.next_run_at is None:
                nxt = self.compute_next(s, now)
                s.next_run_at = nxt.isoformat() if nxt else None

            if s.next_run_at is None:
                continue

            try:
                nxt_dt = datetime.fromisoformat(s.next_run_at)
                if nxt_dt.tzinfo is None:
                    nxt_dt = nxt_dt.replace(tzinfo=timezone.utc)
            except Exception:
                # Recompute on parse errors.
                nxt_dt = self.compute_next(s, now) or (now + timedelta(days=3650))

            if now >= nxt_dt:
                run_id = uuid.uuid4().hex
                wf = load_workflow(s.workflow_path)
                self.runner.run(
                    wf=wf,
                    run_id=run_id,
                    org_id=s.org_id,
                    artifacts_root=self.artifacts_root,
                    state_root=self.state_root,
                )
                s.last_run_at = iso_utc_now()
                s.next_run_at = None  # recompute next tick
                fired.append((s, run_id))

        return fired

    def run_forever(
        self,
        *,
        schedules_path: str,
        poll_s: float = 1.0,
    ) -> None:
        while True:
            schedules = load_schedules(schedules_path)
            self.tick(schedules)
            save_schedules(schedules_path, schedules)
            time.sleep(poll_s)

