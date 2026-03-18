from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


@dataclass(frozen=True)
class Role:
    name: str
    permissions: Set[str]


DEFAULT_ROLES: Dict[str, Role] = {
    "owner": Role("owner", {"*"}),
    "admin": Role("admin", {"billing:write", "users:write", "projects:write", "usage:read"}),
    "member": Role("member", {"projects:write", "usage:read"}),
    "viewer": Role("viewer", {"usage:read"}),
}


def has_permission(role_name: str, perm: str) -> bool:
    role = DEFAULT_ROLES.get(role_name)
    if not role:
        return False
    return "*" in role.permissions or perm in role.permissions


