from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def winner(b: List[str]) -> Optional[str]:
    for a, c, d in WIN_LINES:
        if b[a] != "." and b[a] == b[c] == b[d]:
            return b[a]
    if "." not in b:
        return "D"
    return None


def legal_moves(b: List[str]) -> List[int]:
    return [i for i, v in enumerate(b) if v == "."]


def next_player(p: str) -> str:
    return "O" if p == "X" else "X"


@dataclass
class Node:
    board: Tuple[str, ...]
    player: str
    parent: Optional["Node"] = None
    move: Optional[int] = None
    children: Dict[int, "Node"] = field(default_factory=dict)
    visits: int = 0
    value: float = 0.0  # from perspective of root player

    def is_terminal(self) -> bool:
        return winner(list(self.board)) is not None

    def expand(self):
        b = list(self.board)
        for m in legal_moves(b):
            if m in self.children:
                continue
            b[m] = self.player
            child = Node(board=tuple(b), player=next_player(self.player), parent=self, move=m)
            b[m] = "."
            self.children[m] = child

    def uct(self, c: float = 1.4) -> float:
        if self.visits == 0:
            return float("inf")
        assert self.parent is not None
        return (self.value / self.visits) + c * math.sqrt(math.log(self.parent.visits + 1) / self.visits)


def rollout(board: Tuple[str, ...], player: str, root_player: str, rng: random.Random) -> float:
    b = list(board)
    p = player
    while True:
        w = winner(b)
        if w is not None:
            if w == "D":
                return 0.0
            return 1.0 if w == root_player else -1.0
        m = rng.choice(legal_moves(b))
        b[m] = p
        p = next_player(p)


def mcts_best_move(board: List[str], player: str, sims: int = 2000, seed: int | None = None) -> int:
    rng = random.Random(seed)
    root = Node(board=tuple(board), player=player)
    root_player = player

    for _ in range(sims):
        node = root
        # selection
        while node.children and not node.is_terminal():
            node = max(node.children.values(), key=lambda n: n.uct())
        # expansion
        if not node.is_terminal():
            node.expand()
            if node.children:
                node = rng.choice(list(node.children.values()))
        # simulation
        result = rollout(node.board, node.player, root_player, rng)
        # backprop
        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

    if not root.children:
        raise ValueError("No legal moves")
    return max(root.children.values(), key=lambda n: n.visits).move  # type: ignore[return-value]


def render(b: List[str]):
    for r in range(3):
        print(" ".join(b[r * 3 : r * 3 + 3]))


def main():
    b = ["."] * 9
    human = "O"
    ai = "X"
    turn = "X"
    print("Tic-tac-toe with MCTS. You are O, AI is X.")
    while winner(b) is None:
        print()
        render(b)
        if turn == human:
            raw = input("Your move (0-8): ").strip()
            try:
                m = int(raw)
            except ValueError:
                continue
            if m not in legal_moves(b):
                continue
            b[m] = human
        else:
            m = mcts_best_move(b, ai, sims=1500, seed=0)
            b[m] = ai
            print(f"AI plays {m}")
        turn = "O" if turn == "X" else "X"

    print()
    render(b)
    w = winner(b)
    if w == "D":
        print("Draw.")
    else:
        print(f"Winner: {w}")


if __name__ == "__main__":
    main()

