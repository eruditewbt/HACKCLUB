from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, Tuple

from gridworld_env import GridWorld, Action


def sarsa(
    env: GridWorld,
    episodes: int = 500,
    alpha: float = 0.3,
    gamma: float = 0.98,
    epsilon: float = 0.1,
    max_steps: int = 500,
    seed: int | None = None,
):
    rng = random.Random(seed)
    Q: Dict[Tuple[Tuple[int, int], Action], float] = defaultdict(float)

    def eps_greedy(s):
        actions = env.actions(s)
        if not actions:
            return None
        if rng.random() < epsilon:
            return rng.choice(actions)
        return max(actions, key=lambda a: Q[(s, a)])

    for _ in range(episodes):
        s = env.reset()
        a = eps_greedy(s)
        for _t in range(max_steps):
            if a is None:
                break
            ns, r, done = env.step(s, a)
            na = eps_greedy(ns)
            target = r if na is None else (r + gamma * Q[(ns, na)])
            Q[(s, a)] = Q[(s, a)] + alpha * (target - Q[(s, a)])
            s, a = ns, na
            if done:
                break

    return Q


