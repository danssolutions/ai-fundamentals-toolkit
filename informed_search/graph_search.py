import heapq
from typing import Any


class Node:
    def __init__(self, state: Any, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # cost so far
        self.h = h  # heuristic estimate
        self.f = g + h

    def path(self):
        node, result = self, [self]
        while node.parent:
            node = node.parent
            result.append(node)
        return list(reversed(result))

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"State: {self.state} - g: {self.g}, h: {self.h}, f: {self.f}"


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item: Node):
        heapq.heappush(self.elements, item)

    def pop(self) -> Node:
        return heapq.heappop(self.elements)

    def empty(self) -> bool:
        return not self.elements


def greedy_best_first_search(start, goal, state_space, heuristic_fn):
    frontier = PriorityQueue()
    node = Node(start, h=heuristic_fn(start))
    frontier.push(node)
    visited = set()

    while not frontier.empty():
        current = frontier.pop()
        if current.state == goal:
            return current.path()

        visited.add(current.state)
        for neighbor in state_space[current.state]:
            if neighbor not in visited:
                h = heuristic_fn(neighbor)
                # g=0 for greedy
                frontier.push(Node(neighbor, current, g=0, h=h))


def a_star_search(start, goal, state_space, cost_fn, heuristic_fn):
    frontier = PriorityQueue()
    node = Node(start, g=0, h=heuristic_fn(start))
    frontier.push(node)
    visited = {}

    while not frontier.empty():
        current = frontier.pop()
        if current.state == goal:
            return current.path()

        visited[current.state] = current.g
        for neighbor in state_space[current.state]:
            g = current.g + cost_fn(current.state, neighbor)
            h = heuristic_fn(neighbor)
            if neighbor not in visited or g < visited[neighbor]:
                frontier.push(Node(neighbor, current, g=g, h=h))


# Example test graph and functions
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': [],
    'F': [],
    'G': ['H', 'I', 'J'],
    'H': [],
    'I': [],
    'J': [],
}

heuristic = {
    'A': 10,
    'B': 8,
    'C': 5,
    'D': 7,
    'E': 4,
    'F': 3,
    'G': 2,
    'H': 1,
    'I': 1,
    'J': 0,
}


def heuristic_fn(state):
    return heuristic[state]


def cost_fn(a, b):
    return 1  # uniform for simplicity


if __name__ == "__main__":
    print("Greedy Best-First:")
    path = greedy_best_first_search('A', 'J', graph, heuristic_fn)
    for node in path:
        print(node)

    print("\nA* Search:")
    path = a_star_search('A', 'J', graph, cost_fn, heuristic_fn)
    for node in path:
        print(node)
