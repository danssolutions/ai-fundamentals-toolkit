from graph_search import a_star_search


def generate_vacuum_state_space():
    locations = ['A', 'B']
    dirt_status = ['Clean', 'Dirty']
    state_space = {}

    for loc in locations:
        for a_stat in dirt_status:
            for b_stat in dirt_status:
                state = (loc, a_stat, b_stat)
                successors = []

                # Suck current square
                if loc == 'A' and a_stat == 'Dirty':
                    successors.append(('A', 'Clean', b_stat))
                elif loc == 'B' and b_stat == 'Dirty':
                    successors.append(('B', a_stat, 'Clean'))

                # Move
                if loc == 'A':
                    successors.append(('B', a_stat, b_stat))
                else:
                    successors.append(('A', a_stat, b_stat))

                state_space[state] = successors

    return state_space


def cost_fn(a, b):
    return 1  # constant cost for all moves


def heuristic_fn(state):
    loc, a_stat, b_stat = state
    dirty_count = (a_stat == 'Dirty') + (b_stat == 'Dirty')
    return dirty_count  # estimate = # of remaining tasks


def print_path(path):
    print("Solution path:")
    for node in path:
        print(node)
    print(f"Total cost: {path[-1].g}")
    print(f"Explored nodes: {len(path)}")


if __name__ == '__main__':
    state_space = generate_vacuum_state_space()
    initial = ('A', 'Dirty', 'Dirty')
    goal = ('A', 'Clean', 'Clean')

    print("Vacuum Cleaner A* Search:")
    path = a_star_search(initial, goal, state_space, cost_fn, heuristic_fn)
    print_path(path)
