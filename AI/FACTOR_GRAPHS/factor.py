from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


Assignment = Tuple[Tuple[str, str], ...]  # sorted (var, value) pairs


def _as_assignment(mapping: Mapping[str, str]) -> Assignment:
    return tuple(sorted(mapping.items()))


def _merge_assignments(a: Assignment, b: Assignment) -> Dict[str, str]:
    out: Dict[str, str] = dict(a)
    for k, v in b:
        if k in out and out[k] != v:
            raise ValueError(f"Inconsistent assignment for {k}: {out[k]} vs {v}")
        out[k] = v
    return out


@dataclass(frozen=True)
class Factor:
    """
    Discrete factor over a set of variables.

    - `vars`: ordered list of variables
    - `domains`: var -> list of possible string values
    - `table`: mapping from assignment (sorted pairs) to weight/probability
    """

    vars: Tuple[str, ...]
    domains: Mapping[str, Tuple[str, ...]]
    table: Mapping[Assignment, float]

    @staticmethod
    def from_fn(
        vars: Sequence[str],
        domains: Mapping[str, Sequence[str]],
        fn,
    ) -> "Factor":
        vars_t = tuple(vars)
        dom_t = {k: tuple(v) for k, v in domains.items()}
        table: Dict[Assignment, float] = {}
        for values in product(*[dom_t[v] for v in vars_t]):
            asg = {var: val for var, val in zip(vars_t, values)}
            table[_as_assignment(asg)] = float(fn(asg))
        return Factor(vars=vars_t, domains=dom_t, table=table)

    def value(self, assignment: Mapping[str, str]) -> float:
        key = _as_assignment({k: assignment[k] for k in self.vars})
        return float(self.table.get(key, 0.0))

    def normalize(self) -> "Factor":
        total = float(sum(self.table.values()))
        if total <= 0.0:
            return self
        return Factor(self.vars, self.domains, {k: v / total for k, v in self.table.items()})

    def reduce(self, evidence: Mapping[str, str]) -> "Factor":
        keep_vars = tuple(v for v in self.vars if v not in evidence)
        if keep_vars == self.vars:
            return self

        new_domains = {k: self.domains[k] for k in keep_vars}
        new_table: Dict[Assignment, float] = {}
        for key, val in self.table.items():
            asg = dict(key)
            ok = True
            for ev_k, ev_v in evidence.items():
                if ev_k in asg and asg[ev_k] != ev_v:
                    ok = False
                    break
            if not ok:
                continue
            reduced = {k: asg[k] for k in keep_vars}
            new_table[_as_assignment(reduced)] = new_table.get(_as_assignment(reduced), 0.0) + float(val)
        return Factor(keep_vars, new_domains, new_table)

    def sum_out(self, var: str) -> "Factor":
        if var not in self.vars:
            return self
        keep_vars = tuple(v for v in self.vars if v != var)
        new_domains = {k: self.domains[k] for k in keep_vars}
        new_table: Dict[Assignment, float] = {}

        for key, val in self.table.items():
            asg = dict(key)
            reduced = {k: asg[k] for k in keep_vars}
            rk = _as_assignment(reduced)
            new_table[rk] = new_table.get(rk, 0.0) + float(val)

        return Factor(keep_vars, new_domains, new_table)

    def multiply(self, other: "Factor") -> "Factor":
        new_vars: List[str] = list(self.vars)
        for v in other.vars:
            if v not in new_vars:
                new_vars.append(v)
        new_vars_t = tuple(new_vars)

        new_domains: Dict[str, Tuple[str, ...]] = {}
        for v in new_vars_t:
            if v in self.domains and v in other.domains:
                if tuple(self.domains[v]) != tuple(other.domains[v]):
                    raise ValueError(f"Domain mismatch for {v}")
                new_domains[v] = tuple(self.domains[v])
            elif v in self.domains:
                new_domains[v] = tuple(self.domains[v])
            else:
                new_domains[v] = tuple(other.domains[v])

        new_table: Dict[Assignment, float] = {}
        # brute force join over assignments; fine for tiny demos
        for k1, v1 in self.table.items():
            for k2, v2 in other.table.items():
                merged = _merge_assignments(k1, k2)
                new_key = _as_assignment({k: merged[k] for k in new_vars_t})
                new_table[new_key] = new_table.get(new_key, 0.0) + float(v1) * float(v2)

        return Factor(new_vars_t, new_domains, new_table)

    def marginal(self, vars: Sequence[str]) -> "Factor":
        f = self
        for v in list(self.vars):
            if v not in vars:
                f = f.sum_out(v)
        return f

    def argmax(self) -> Mapping[str, str]:
        best_key = None
        best_val = float("-inf")
        for k, v in self.table.items():
            if float(v) > best_val:
                best_val = float(v)
                best_key = k
        return dict(best_key or ())


