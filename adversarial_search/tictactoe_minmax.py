from enum import Enum
from typing import List


class Symbols(Enum):
    X = "X"
    O = "O"
    UNPLACED = "i"

    def __str__(self):
        return self.value

    @classmethod
    def placed(cls):
        return cls.X, cls.O


type Board = List[Symbols]


def is_terminal(state: Board) -> bool:
    return utility_of(state) != 0 or all(cell != Symbols.UNPLACED for cell in state)


def utility_of(state: Board) -> int:
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diags
    ]
    for a, b, c in wins:
        if state[a] == state[b] == state[c] != Symbols.UNPLACED:
            return 1 if state[a] == Symbols.X else -1
    return 0


def successors_of(state: Board) -> List[tuple[int, Board]]:
    moves = []
    current_player = Symbols.X if state.count(
        Symbols.X) == state.count(Symbols.O) else Symbols.O
    for i in range(9):
        if state[i] == Symbols.UNPLACED:
            new_state = state.copy()
            new_state[i] = current_player
            moves.append((i, new_state))
    return moves


def minmax_decision(state: Board) -> int:
    def max_value(s: Board) -> int:
        if is_terminal(s):
            return utility_of(s)
        return max(min_value(sp) for _, sp in successors_of(s))

    def min_value(s: Board) -> int:
        if is_terminal(s):
            return utility_of(s)
        return min(max_value(sp) for _, sp in successors_of(s))

    return max(successors_of(state), key=lambda a: min_value(a[1]))[0]


def display(state: Board):
    print("-----")
    for i in range(0, 9, 3):
        row = state[i:i + 3]
        print("|" + "|".join(str(c.value if isinstance(c, Symbols) else c)
              for c in row) + "|")


def main():
    board = [Symbols.UNPLACED] * 9
    while not is_terminal(board):
        board[minmax_decision(board)] = Symbols.X
        if not is_terminal(board):
            display(board)
            move = int(input("Your move? "))
            if board[move] == Symbols.UNPLACED:
                board[move] = Symbols.O
    display(board)


if __name__ == "__main__":
    main()
