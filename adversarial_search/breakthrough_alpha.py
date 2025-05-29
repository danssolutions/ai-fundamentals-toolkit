from typing import List
import copy

PLAYER_ONE = "W"
PLAYER_TWO = "B"
EMPTY = "."

type Board = List[List[str]]


def initial_board(size: int = 4) -> Board:
    board = [[EMPTY for _ in range(size)] for _ in range(size)]
    for i in range(size):
        board[0][i] = PLAYER_TWO
        board[-1][i] = PLAYER_ONE
    return board


def display(board: Board):
    for row in board:
        print(" ".join(row))
    print()


def get_opponent(player: str) -> str:
    return PLAYER_ONE if player == PLAYER_TWO else PLAYER_TWO


def is_terminal(board: Board, player: str) -> bool:
    size = len(board)
    opponent = get_opponent(player)

    # Win if a pawn reaches opponent's back row
    if player == PLAYER_ONE and PLAYER_ONE in board[0]:
        return True
    if player == PLAYER_TWO and PLAYER_TWO in board[-1]:
        return True

    # Win if opponent has no pieces
    return not any(opponent in row for row in board)


def utility_of(board: Board, player: str) -> int:
    if is_terminal(board, player):
        return 1
    elif is_terminal(board, get_opponent(player)):
        return -1
    return 0


def successors_of(board: Board, player: str) -> List[Board]:
    size = len(board)
    successors = []
    direction = -1 if player == PLAYER_ONE else 1

    for r in range(size):
        for c in range(size):
            if board[r][c] != player:
                continue
            new_r = r + direction

            if 0 <= new_r < size:
                # Forward
                if board[new_r][c] == EMPTY:
                    new_board = copy.deepcopy(board)
                    new_board[r][c] = EMPTY
                    new_board[new_r][c] = player
                    successors.append(new_board)

                # Diagonal captures
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < size and board[new_r][nc] == get_opponent(player):
                        new_board = copy.deepcopy(board)
                        new_board[r][c] = EMPTY
                        new_board[new_r][nc] = player
                        successors.append(new_board)
    return successors


def alpha_beta_decision(board: Board, player: str) -> Board:
    def max_value(state, alpha, beta, depth):
        if is_terminal(state, player) or depth == 4:
            return utility_of(state, player)
        v = float('-inf')
        for s in successors_of(state, player):
            v = max(v, min_value(s, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        opponent = get_opponent(player)
        if is_terminal(state, opponent) or depth == 4:
            return utility_of(state, player)
        v = float('inf')
        for s in successors_of(state, opponent):
            v = min(v, max_value(s, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    return max(successors_of(board, player), key=lambda s: min_value(s, float('-inf'), float('inf'), 0))


def main():
    board = initial_board(4)
    current_player = PLAYER_ONE
    display(board)

    while not is_terminal(board, current_player) and not is_terminal(board, get_opponent(current_player)):
        if current_player == PLAYER_ONE:
            board = alpha_beta_decision(board, PLAYER_ONE)
            print("White (W) moves:")
        else:
            board = alpha_beta_decision(board, PLAYER_TWO)
            print("Black (B) moves:")
        display(board)
        current_player = get_opponent(current_player)

    print(f"Game over. Winner: {get_opponent(current_player)}")


if __name__ == "__main__":
    main()
