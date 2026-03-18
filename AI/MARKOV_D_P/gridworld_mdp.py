from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple


Action = int  # 0=up,1=right,2=down,3=left


@dataclass
class GridWorldMDP:
    width: int
    height: int
    start: Tuple[int, int]
    terminal: Tuple[int, int]
    walls: List[Tuple[int, int]]
    step_reward: float = -0.04
    terminal_reward: float = 1.0
    slip_prob: float = 0.0  # probability of random action instead of intended

    def start_state(self) -> Tuple[int, int]:
        return self.start

    def is_end(self, state: Tuple[int, int]) -> bool:
        return state == self.terminal

    def actions(self, state: Tuple[int, int]) -> List[Action]:
        if self.is_end(state):
            return []
        return [0, 1, 2, 3]

    def discount(self) -> float:
        return 0.98

    def states(self) -> Iterable[Tuple[int, int]]:
        wset = set(self.walls)
        for y in range(self.height):
            for x in range(self.width):
                s = (x, y)
                if s in wset:
                    continue
                yield s

    def succ_prob_reward(self, state: Tuple[int, int], action: Action):
        if self.is_end(state):
            return [(state, 1.0, 0.0)]

        actions = [action]
        if self.slip_prob > 0.0:
            # uniform over the other 3 actions
            other = [a for a in [0, 1, 2, 3] if a != action]
            outcomes = []
            for a in other:
                ns, r = self._move(state, a)
                outcomes.append((ns, self.slip_prob / 3.0, r))
            ns, r = self._move(state, action)
            outcomes.append((ns, 1.0 - self.slip_prob, r))
            return outcomes

        ns, r = self._move(state, action)
        return [(ns, 1.0, r)]

    def _move(self, state: Tuple[int, int], action: Action):
        x, y = state
        nx, ny = x, y
        if action == 0:
            ny -= 1
        elif action == 1:
            nx += 1
        elif action == 2:
            ny += 1
        else:
            nx -= 1
        if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or (nx, ny) in set(self.walls):
            nx, ny = x, y
        ns = (nx, ny)
        done = self.is_end(ns)
        r = self.terminal_reward if done else self.step_reward
        return ns, r


