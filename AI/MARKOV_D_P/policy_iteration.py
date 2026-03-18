from __future__ import annotations

from typing import Dict, Tuple, TypeVar

from mdp_base import MDP, Policy, ValueFn, q_value


S = TypeVar("S")
A = TypeVar("A")


def policy_evaluation(mdp: MDP[S, A], policy: Policy[S, A], tol: float = 1e-10) -> ValueFn[S]:
    V: ValueFn[S] = {s: 0.0 for s in mdp.states()}
    while True:
        delta = 0.0
        newV: ValueFn[S] = {}
        for s in mdp.states():
            if mdp.is_end(s):
                newV[s] = 0.0
                continue
            a = policy[s]
            v = q_value(mdp, V, s, a)
            newV[s] = v
            delta = max(delta, abs(V[s] - v))
        V = newV
        if delta < tol:
            return V


def policy_improvement(mdp: MDP[S, A], V: ValueFn[S]) -> Policy[S, A]:
    pi: Policy[S, A] = {}
    for s in mdp.states():
        if mdp.is_end(s):
            continue
        pi[s] = max(mdp.actions(s), key=lambda a: q_value(mdp, V, s, a))
    return pi


def policy_iteration(mdp: MDP[S, A], max_iters: int = 100) -> Tuple[Policy[S, A], ValueFn[S]]:
    # initialize with arbitrary valid actions
    pi: Policy[S, A] = {}
    for s in mdp.states():
        if mdp.is_end(s):
            continue
        acts = mdp.actions(s)
        pi[s] = acts[0]

    for _ in range(max_iters):
        V = policy_evaluation(mdp, pi)
        new_pi = policy_improvement(mdp, V)
        if new_pi == pi:
            return pi, V
        pi = new_pi
    return pi, policy_evaluation(mdp, pi)


