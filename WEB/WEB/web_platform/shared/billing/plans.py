from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Plan:
    key: str
    name: str
    monthly_usd: int
    rpm_limit: int
    seats: int
    features: Dict[str, bool]


PLANS: Dict[str, Plan] = {
    "free": Plan("free", "Free", monthly_usd=0, rpm_limit=30, seats=1, features={"api": True, "teams": False}),
    "pro": Plan("pro", "Pro", monthly_usd=29, rpm_limit=240, seats=5, features={"api": True, "teams": True}),
    "business": Plan("business", "Business", monthly_usd=99, rpm_limit=600, seats=25, features={"api": True, "teams": True}),
}


def get_plan(key: str) -> Optional[Plan]:
    return PLANS.get(key)


def feature_enabled(plan_key: str, feature: str) -> bool:
    p = get_plan(plan_key)
    if not p:
        return False
    return bool(p.features.get(feature, False))


