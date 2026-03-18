from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from factor import Factor


def _neighbors(undirected_edges: Sequence[Tuple[str, str]]) -> Dict[str, List[str]]:
    n: Dict[str, List[str]] = {}
    for a, b in undirected_edges:
        n.setdefault(a, []).append(b)
        n.setdefault(b, []).append(a)
    return n


def sum_product_tree(
    var_nodes: Sequence[str],
    factor_nodes: Sequence[str],
    edges: Sequence[Tuple[str, str]],
    factors: Mapping[str, Factor],
    evidence: Mapping[str, str] | None = None,
    root: str | None = None,
) -> Mapping[str, Factor]:
    """
    Very small sum-product on a *tree* factor graph.

    Nodes are named strings; edges connect variables <-> factors.
    `factors[factor_node]` provides the factor.
    Returns marginal factors for each variable node.
    """

    evidence = dict(evidence or {})
    nbr = _neighbors(edges)
    if not var_nodes:
        return {}
    if root is None:
        root = var_nodes[0]

    # Messages are Factor objects over the recipient variable.
    msg: Dict[Tuple[str, str], Factor] = {}

    def send(u: str, v: str):
        if (u, v) in msg:
            return

        # Ensure all incoming messages to u except from v are computed
        for w in nbr.get(u, []):
            if w == v:
                continue
            send(w, u)

        if u in factor_nodes:
            # factor -> variable
            f = factors[u]
            f = f.reduce(evidence)
            for w in nbr.get(u, []):
                if w == v:
                    continue
                f = f.multiply(msg[(w, u)])
            # sum out all variables except v
            for var in list(f.vars):
                if var != v:
                    f = f.sum_out(var)
            msg[(u, v)] = f.normalize()
        else:
            # variable -> factor: multiply incoming messages (all are over this variable)
            var = u
            # start with delta if evidence fixes it
            incoming: List[Factor] = []
            if var in evidence:
                dom = {var: factors[nbr[var][0]].domains[var]} if nbr.get(var) else {var: (evidence[var],)}
                incoming.append(Factor.from_fn([var], dom, lambda a: 1.0 if a[var] == evidence[var] else 0.0))
            for w in nbr.get(u, []):
                if w == v:
                    continue
                incoming.append(msg[(w, u)])
            if not incoming:
                # isolated variable
                raise ValueError(f"Isolated variable node: {var}")
            out = incoming[0]
            for f in incoming[1:]:
                out = out.multiply(f)
            # marginal over var is already a factor over var
            msg[(u, v)] = out.marginal([var]).normalize()

    # schedule all messages by rooting and sending along edges in both directions
    for a, b in edges:
        send(a, b)
        send(b, a)

    # compute variable marginals by multiplying all factor->var messages
    marginals: Dict[str, Factor] = {}
    for var in var_nodes:
        incoming = [msg[(fnode, var)] for fnode in nbr.get(var, [])]
        if not incoming:
            continue
        out = incoming[0]
        for f in incoming[1:]:
            out = out.multiply(f)
        marginals[var] = out.marginal([var]).normalize()
    return marginals


