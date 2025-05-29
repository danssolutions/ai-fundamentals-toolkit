from itertools import product
from search import Searcher, StateSpace

sides = ['W', 'E']


def is_valid(state):
    f, w, g, c = state
    # Goat alone with wolf or cabbage without farmer
    if f != g and (g == w or g == c):
        return False
    return True


def generate_successors(state):
    f, w, g, c = state
    new_side = 'E' if f == 'W' else 'W'
    options = []

    # Farmer alone
    new_state = (new_side, w, g, c)
    if is_valid(new_state):
        options.append(new_state)

    # Farmer with wolf
    if f == w:
        new_state = (new_side, new_side, g, c)
        if is_valid(new_state):
            options.append(new_state)

    # Farmer with goat
    if f == g:
        new_state = (new_side, w, new_side, c)
        if is_valid(new_state):
            options.append(new_state)

    # Farmer with cabbage
    if f == c:
        new_state = (new_side, w, g, new_side)
        if is_valid(new_state):
            options.append(new_state)

    return options


# Construct state space graph

all_states = list(product(sides, repeat=4))
state_space = {
    s: generate_successors(s)
    for s in all_states
    if is_valid(s)
}

initial = ('W', 'W', 'W', 'W')
goal = ('E', 'E', 'E', 'E')

if __name__ == '__main__':
    print("Farmer River Crossing Problem:")
    searcher = Searcher(initial, goal, StateSpace(state_space))
    searcher.run(insert_as_first=False)
