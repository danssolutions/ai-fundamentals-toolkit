from typing import List, Tuple, Dict
from enums import LocationState, Location, States, Action

type Percept = LocationState
type Percepts = list[Percept]

total_percepts: Percepts = []

# Helper combos:
clean_A = (Location.A, States.CLEAN)
dirty_A = (Location.A, States.DIRTY)
clean_B = (Location.B, States.CLEAN)
dirty_B = (Location.B, States.DIRTY)

type LookupTable = dict[tuple[Percept, ...], Action]

# Q: How many entries would there be needed for a stateless agent?
# In this example there would be 2 locations x 2 states = 4 possible current percepts = 4 table entries.
# Q: How many for an agent lifetime of T steps?
# Each percept is drawn from 4 possible options. For a T-length history, number of table entries = 4^T (exponential in time steps).
table_definition: LookupTable = {
    (clean_A,): Action.RIGHT,
    (dirty_A,): Action.SUCK,
    (clean_B,): Action.LEFT,
    (dirty_B,): Action.SUCK,
    (clean_A, clean_A): Action.RIGHT,
    (clean_A, dirty_A): Action.SUCK,
    # ...
    (clean_A, clean_A, clean_A): Action.RIGHT,
    (clean_A, clean_A, dirty_A): Action.SUCK,
    (clean_A, dirty_A, clean_B): Action.LEFT,
    # ...
}


def LOOKUP(percepts: Percepts, table: LookupTable) -> Action:
    """
    Lookup appropriate action for percepts
    :return: Action from table or Action.NO_OP if no suitable action found
    """
    return table.get(tuple(percepts), Action.NO_OP)


# Determine action based on table and percepts
def TABLE_DRIVEN_AGENT(percept: Percept) -> Action:
    total_percepts.append(percept)  # Add percept
    # Lookup appropriate action for percepts
    return LOOKUP(total_percepts, table_definition)


def run():  # run agent on several sequential percepts
    action_space = 14
    print(f"{"Action":{action_space}s}| Percepts")
    print(f"{TABLE_DRIVEN_AGENT(clean_A):{action_space}s}| {total_percepts}")
    print(f"{TABLE_DRIVEN_AGENT(dirty_A):{action_space}s}| {total_percepts}")
    print(f"{TABLE_DRIVEN_AGENT(clean_B):{action_space}s}| {total_percepts}")
    print(f"{TABLE_DRIVEN_AGENT(dirty_B):{action_space}s}| {total_percepts}")


if __name__ == '__main__':
    run()
