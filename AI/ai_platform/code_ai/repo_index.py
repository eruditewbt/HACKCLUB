from __future__ import annotations

import ast
import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Symbol:
    kind: str
    name: str
    file: str
    line: int


def index_python_repo(root: str, *, max_files: int = 5000) -> List[Symbol]:
    symbols: List[Symbol] = []
    n = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(dirpath, fn)
            n += 1
            if n > max_files:
                return symbols
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    src = f.read()
                tree = ast.parse(src)
            except Exception:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    symbols.append(Symbol(kind='function', name=node.name, file=path, line=getattr(node, 'lineno', 1)))
                elif isinstance(node, ast.ClassDef):
                    symbols.append(Symbol(kind='class', name=node.name, file=path, line=getattr(node, 'lineno', 1)))
    return symbols


def search_symbols(symbols: List[Symbol], query: str, *, limit: int = 30) -> List[Symbol]:
    q = (query or '').lower().strip()
    if not q:
        return []
    out = [s for s in symbols if q in s.name.lower()]
    return out[:limit]
