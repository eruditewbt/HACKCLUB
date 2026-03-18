from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


Action = int  # 0=up,1=right,2=down,3=left


@dataclass
class GridWorld:
    width: int
    height: int
    start: Tuple[int, int]
    terminal: Tuple[int, int]
    walls: List[Tuple[int, int]]
    step_reward: float = -0.04
    terminal_reward: float = 1.0

    def reset(self) -> Tuple[int, int]:
        return self.start

    def is_terminal(self, s: Tuple[int, int]) -> bool:
        return s == self.terminal

    def actions(self, s: Tuple[int, int]) -> List[Action]:
        if self.is_terminal(s):
            return []
        return [0, 1, 2, 3]

    def step(self, s: Tuple[int, int], a: Action) -> Tuple[Tuple[int, int], float, bool]:
        if self.is_terminal(s):
            return s, 0.0, True

        x, y = s
        nx, ny = x, y
        if a == 0:
            ny -= 1
        elif a == 1:
            nx += 1
        elif a == 2:
            ny += 1
        else:
            nx -= 1

        if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or (nx, ny) in set(self.walls):
            nx, ny = x, y

        ns = (nx, ny)
        done = self.is_terminal(ns)
        r = self.terminal_reward if done else self.step_reward
        return ns, r, done


def render_policy(width: int, height: int, terminal: Tuple[int, int], walls: List[Tuple[int, int]], pi):
    arrows = {0: "^", 1: ">", 2: "v", 3: "<"}
    wset = set(walls)
    for y in range(height):
        row = []
        for x in range(width):
            s = (x, y)
            if s in wset:
                row.append("#")
            elif s == terminal:
                row.append("T")
            else:
                a = pi.get(s, None)
                row.append(arrows.get(a, "."))
        print(" ".join(row))


