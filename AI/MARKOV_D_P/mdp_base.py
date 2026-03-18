from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Protocol, Tuple, TypeVar


S = TypeVar("S")
A = TypeVar("A")


class MDP(Protocol[S, A]):
    def start_state(self) -> S: ...
    def is_end(self, state: S) -> bool: ...
    def actions(self, state: S) -> List[A]: ...
    def succ_prob_reward(self, state: S, action: A) -> List[Tuple[S, float, float]]: ...
    def discount(self) -> float: ...
    def states(self) -> Iterable[S]: ...


Policy = Dict[S, A]
ValueFn = Dict[S, float]


def q_value(mdp: MDP[S, A], V: ValueFn, state: S, action: A) -> float:
    return sum(prob * (reward + mdp.discount() * V[new_state]) for new_state, prob, reward in mdp.succ_prob_reward(state, action))


