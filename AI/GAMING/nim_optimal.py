from __future__ import annotations

from typing import List, Tuple


def nim_xor(piles: List[int]) -> int:
    x = 0
    for p in piles:
        x ^= p
    return x


def optimal_move(piles: List[int]) -> Tuple[int, int]:
    """
    Returns (pile_index, remove_count). If already losing (xor==0),
    removes 1 from the first non-empty pile.
    """
    x = nim_xor(piles)
    if x == 0:
        for i, p in enumerate(piles):
            if p > 0:
                return i, 1
        return 0, 0

    for i, p in enumerate(piles):
        target = p ^ x
        if target < p:
            return i, p - target
    return 0, 0


def apply_move(piles: List[int], move: Tuple[int, int]) -> List[int]:
    i, remove = move
    new = list(piles)
    new[i] = max(0, new[i] - remove)
    return new


def is_terminal(piles: List[int]) -> bool:
    return all(p == 0 for p in piles)


def main():
    piles = [3, 4, 5]
    player = 1
    print("Nim (normal play). Remove any positive number from one pile. Last move wins.")
    print("Type 'auto' to let the solver play your turn.")
    while not is_terminal(piles):
        print(f"\nPiles: {piles} (xor={nim_xor(piles)})")
        if player == 1:
            raw = input("Your move as 'pile remove' (e.g. '1 2') or 'auto': ").strip().lower()
            if raw == "auto":
                mv = optimal_move(piles)
            else:
                parts = raw.split()
                if len(parts) != 2:
                    print("Invalid input.")
                    continue
                try:
                    pi = int(parts[0])
                    rm = int(parts[1])
                except ValueError:
                    print("Invalid numbers.")
                    continue
                if pi < 0 or pi >= len(piles) or rm <= 0 or rm > piles[pi]:
                    print("Illegal move.")
                    continue
                mv = (pi, rm)
        else:
            mv = optimal_move(piles)
            print(f"Solver plays: pile={mv[0]} remove={mv[1]}")

        piles = apply_move(piles, mv)
        player *= -1

    winner = -player
    print("\nGame over.")
    print("You win!" if winner == 1 else "Solver wins!")


if __name__ == "__main__":
    main()

