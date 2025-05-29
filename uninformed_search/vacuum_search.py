from search import Searcher, StateSpace

# Full state space for 2-location vacuum cleaner problem
vacuum_state_space = {
    ('A', 'Dirty', 'Dirty'): [
        ('A', 'Clean', 'Dirty'),  # Suck at A
        ('B', 'Dirty', 'Dirty')   # Move to B
    ],
    ('A', 'Clean', 'Dirty'): [
        ('B', 'Clean', 'Dirty')
    ],
    ('A', 'Dirty', 'Clean'): [
        ('A', 'Clean', 'Clean'),
        ('B', 'Dirty', 'Clean')
    ],
    ('A', 'Clean', 'Clean'): [
        ('B', 'Clean', 'Clean')
    ],

    ('B', 'Dirty', 'Dirty'): [
        ('B', 'Dirty', 'Clean'),  # Suck at B
        ('A', 'Dirty', 'Dirty')   # Move to A
    ],
    ('B', 'Dirty', 'Clean'): [
        ('B', 'Clean', 'Clean'),
        ('A', 'Dirty', 'Clean')
    ],
    ('B', 'Clean', 'Dirty'): [
        ('B', 'Clean', 'Clean'),
        ('A', 'Clean', 'Dirty')
    ],
    ('B', 'Clean', 'Clean'): [
        ('A', 'Clean', 'Clean')
    ],
}

initial_state = ('A', 'Dirty', 'Dirty')
goal_state = ('A', 'Clean', 'Clean')

if __name__ == '__main__':
    print("Vacuum World BFS:")
    searcher = Searcher(initial_state, goal_state,
                        StateSpace(vacuum_state_space))
    searcher.run(insert_as_first=False)
