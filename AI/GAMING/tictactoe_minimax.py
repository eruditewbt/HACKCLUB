from __future__ import annotations

from typing import List, Optional, Tuple


Board = List[str]  # 9 cells, values: "X", "O", "."


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


def winner(b: Board) -> Optional[str]:
    for a, c, d in WIN_LINES:
        if b[a] != "." and b[a] == b[c] == b[d]:
            return b[a]
    if "." not in b:
        return "D"
    return None


def legal_moves(b: Board) -> List[int]:
    return [i for i, v in enumerate(b) if v == "."]


def render(b: Board):
    for r in range(3):
        print(" ".join(b[r * 3 : r * 3 + 3]))


def minimax(b: Board, player: str, alpha: int, beta: int) -> Tuple[int, Optional[int]]:
    w = winner(b)
    if w == "X":
        return 1, None
    if w == "O":
        return -1, None
    if w == "D":
        return 0, None

    if player == "X":
        best_score, best_move = -10, None
        for m in legal_moves(b):
            b[m] = "X"
            score, _ = minimax(b, "O", alpha, beta)
            b[m] = "."
            if score > best_score:
                best_score, best_move = score, m
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score, best_move = 10, None
        for m in legal_moves(b):
            b[m] = "O"
            score, _ = minimax(b, "X", alpha, beta)
            b[m] = "."
            if score < best_score:
                best_score, best_move = score, m
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move


def best_move(b: Board, player: str) -> int:
    _, m = minimax(b, player, alpha=-10, beta=10)
    assert m is not None
    return m


def main():
    b = ["."] * 9
    human = "O"
    ai = "X"
    turn = "X"
    print("Tic-tac-toe. Cells are 0..8. You are O, AI is X.")
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
            m = best_move(b, ai)
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

