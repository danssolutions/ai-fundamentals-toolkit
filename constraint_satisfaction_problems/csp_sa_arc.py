from states import SAStates
from colors import Color
from typing import Dict, List, Any, Tuple
from collections import deque
import copy


def constraint_function(var1, val1, var2, val2):
    return val1 != val2 or var1 == var2


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables: List[Any] = variables
        self.domains: Dict[Any, List[Color]] = domains
        self.neighbours: Dict[Any, List[Any]] = neighbours
        self.constraints: Dict[Any, Any] = constraints

    def backtracking_search(self, use_forward_checking: bool = False, use_ac3: bool = False):
        domains = copy.deepcopy(self.domains)

        if use_ac3:
            if not self.ac3(domains):
                print("AC-3 failed to establish arc consistency.")
                return None

        return self.recursive_backtracking({}, domains, use_forward_checking)

    def recursive_backtracking(self, assignment, domains, use_forward_checking):
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment, domains):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                local_domains = copy.deepcopy(domains)

                if use_forward_checking:
                    if not self.forward_check(var, value, assignment, local_domains):
                        del assignment[var]
                        continue

                result = self.recursive_backtracking(
                    assignment, local_domains, use_forward_checking)
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

    def order_domain_values(self, variable, assignment, domains):
        return domains[variable][:]

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

    def forward_check(self, var, value, assignment, domains):
        constraint = self.constraints[var]
        for neighbor in self.neighbours[var]:
            if neighbor in assignment:
                continue

            revised_domain = [val for val in domains[neighbor]
                              if constraint(var, value, neighbor, val)]

            if not revised_domain:
                return False
            domains[neighbor] = revised_domain
        return True

    def ac3(self, domains) -> bool:
        queue: deque[Tuple[Any, Any]] = deque(
            (xi, xj) for xi in self.variables for xj in self.neighbours[xi])

        while queue:
            xi, xj = queue.popleft()
            if self.revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in self.neighbours[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, domains, xi, xj) -> bool:
        revised = False
        constraint = self.constraints[xi]
        for x in domains[xi][:]:
            if not any(constraint(xi, x, xj, y) for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised


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

    print("Solving with arc consistency and forward checking...\n")
    result = csp.backtracking_search(use_forward_checking=True, use_ac3=True)
    if result:
        for state, color in result.items():
            print(f"{state.name}: {color.name}")
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
