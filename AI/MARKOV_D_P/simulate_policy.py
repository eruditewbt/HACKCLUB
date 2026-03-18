from __future__ import annotations

import random
from typing import Dict, Tuple

from gridworld_mdp import GridWorldMDP
from policy_iteration import policy_iteration


ARROWS = {0: "^", 1: ">", 2: "v", 3: "<"}


def render_policy(mdp: GridWorldMDP, pi: Dict[Tuple[int, int], int]):
    wset = set(mdp.walls)
    for y in range(mdp.height):
        row = []
        for x in range(mdp.width):
            s = (x, y)
            if s in wset:
                row.append("#")
            elif s == mdp.terminal:
                row.append("T")
            else:
                row.append(ARROWS.get(pi.get(s, -1), "."))
        print(" ".join(row))


def rollout(mdp: GridWorldMDP, pi: Dict[Tuple[int, int], int], episodes: int = 5, seed: int = 0):
    rng = random.Random(seed)
    for ep in range(episodes):
        s = mdp.start_state()
        total = 0.0
        steps = 0
        while not mdp.is_end(s) and steps < 200:
            a = pi.get(s, rng.choice(mdp.actions(s)))
            outcomes = mdp.succ_prob_reward(s, a)
            r = rng.random()
            cum = 0.0
            ns = s
            rew = 0.0
            for st, p, rw in outcomes:
                cum += p
                if r <= cum:
                    ns, rew = st, rw
                    break
            s = ns
            total += rew
            steps += 1
        print(f"episode={ep} return={total:.3f} steps={steps}")


def main():
    mdp = GridWorldMDP(
        width=5,
        height=4,
        start=(0, 3),
        terminal=(4, 0),
        walls=[(1, 1), (2, 1), (3, 1)],
        step_reward=-0.03,
        terminal_reward=1.0,
        slip_prob=0.1,
    )
    pi, V = policy_iteration(mdp)
    print("Policy iteration policy:")
    render_policy(mdp, pi)
    print("\nRollouts:")
    rollout(mdp, pi)


if __name__ == "__main__":
    main()

