from states import SAStates
from colors import Color
from typing import Dict, List, Any


def constraint_function(var1, val1, var2, val2):
    return val1 != val2 or var1 == var2


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables: List[Any] = variables
        self.domains: Dict[Any, List[Color]] = domains
        self.neighbours: Dict[Any, List[Any]] = neighbours
        self.constraints: Dict[Any, Any] = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def is_complete(self, assignment):
        return len(assignment) == len(self.variables)

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def order_domain_values(self, variable, assignment):
        return self.domains[variable][:]

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True
        constraint = self.constraints[variable]
        for neighbour in self.neighbours[variable]:
            if neighbour in assignment:
                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_south_america_csp():
    variables = list(SAStates)
    domains = {
        var: [Color.Red, Color.Green, Color.Blue, Color.Yellow]
        for var in variables
    }

    neighbours = {
        SAStates.ARG: [SAStates.BOL, SAStates.BRA, SAStates.CHI, SAStates.PAR, SAStates.URU],
        SAStates.BOL: [SAStates.ARG, SAStates.BRA, SAStates.CHI, SAStates.PAR, SAStates.PER],
        SAStates.BRA: [SAStates.ARG, SAStates.BOL, SAStates.COL, SAStates.GUY, SAStates.PAR,
                       SAStates.PER, SAStates.SUR, SAStates.URU, SAStates.VEN],
        SAStates.CHI: [SAStates.ARG, SAStates.BOL, SAStates.PER],
        SAStates.COL: [SAStates.BRA, SAStates.ECU, SAStates.PER, SAStates.VEN],
        SAStates.ECU: [SAStates.COL, SAStates.PER],
        SAStates.GUY: [SAStates.BRA, SAStates.SUR, SAStates.VEN],
        SAStates.PAR: [SAStates.ARG, SAStates.BOL, SAStates.BRA],
        SAStates.PER: [SAStates.BOL, SAStates.BRA, SAStates.CHI, SAStates.COL, SAStates.ECU],
        SAStates.SUR: [SAStates.BRA, SAStates.GUY],
        SAStates.URU: [SAStates.ARG, SAStates.BRA],
        SAStates.VEN: [SAStates.BRA, SAStates.COL, SAStates.GUY],
    }

    constraints = {var: constraint_function for var in variables}
    return CSP(variables, domains, neighbours, constraints)


def main():
    csp = create_south_america_csp()
    result = csp.backtracking_search()
    if result:
        for state, color in result.items():
            print(f"{state.name}: {color.name}")
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
