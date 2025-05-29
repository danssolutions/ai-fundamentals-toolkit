from typing import List

type Piles = List[int]


def alpha_beta_decision(state: Piles) -> Piles:
    def max_value(state, alpha, beta):
        if is_terminal(state):
            return utility_of(state)
        v = float('-inf')
        for successor in successors_of(state):
            v = max(v, min_value(successor, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if is_terminal(state):
            return utility_of(state)
        v = float('inf')
        for successor in successors_of(state):
            v = min(v, max_value(successor, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    return min(successors_of(state), key=lambda s: max_value(s, float('-inf'), float('inf')))


def is_terminal(state: Piles) -> bool:
    return all(pile <= 2 for pile in state)


def utility_of(state: Piles) -> int:
    # +1 if MIN wins (i.e. computer wins), -1 if MAX wins
    return 1 if is_terminal(state) else 0


def successors_of(state: Piles) -> List[Piles]:
    successors = []
    for i, pile in enumerate(state):
        if pile > 2:
            for a, b in split_pile_options(pile):
                new_state = state[:i] + [a, b] + state[i+1:]
                successors.append(sorted(new_state, reverse=True))
    return successors


def split_pile_options(pile: int) -> List[tuple[int, int]]:
    return [(a, pile - a) for a in range(1, pile) if a != pile - a]


def main():
    state = [7]
    while not is_terminal(state):
        print(f"\nCurrent state: {state}")
        state = alpha_beta_decision(state)
        print("Computer (MIN) moves.")
        print(f"New state: {state}")
        if is_terminal(state):
            print("Computer wins. You lose.")
            break
        state = user_select_pile(state)
    else:
        print("You win! Computer has no valid move.")


def user_select_pile(state: Piles) -> Piles:
    print("Select a pile to split:")
    for i, pile in enumerate(state):
        print(f"{i}: {pile}")
    idx = int(input("Pile index: "))
    pile = state[idx]
    if pile <= 2:
        print("Invalid. Pile must be > 2.")
        return state

    options = split_pile_options(pile)
    print("Split options:")
    for j, (a, b) in enumerate(options):
        print(f"{j}: {a}, {b}")
    opt = int(input("Split index: "))
    a, b = options[opt]

    return sorted(state[:idx] + [a, b] + state[idx+1:], reverse=True)


if __name__ == '__main__':
    main()
