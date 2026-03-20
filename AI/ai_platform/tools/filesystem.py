from __future__ import annotations

import os
from typing import List


def list_files(root: str, *, limit: int = 500) -> List[str]:
    out: List[str] = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            out.append(os.path.join(dirpath, fn))
            if len(out) >= limit:
                return out
    return out
