from typing import Self, Any


class StateSpace:
    def __init__(self, state_space: dict = None):
        self.state_space = state_space

    def successor(self, state: Any):
        if self.state_space is None:
            print("No state space set")
        return self.state_space[state]


class Node:
    def __init__(self, state: Any, parent: Self = None, depth: int = 0):
        self.state = state
        self.parent_node = parent
        self.depth = depth

    def path(self) -> list[Self]:
        """Create a list of nodes from the root to this node."""
        current_node = self
        path = [self]
        while current_node.parent_node:
            current_node = current_node.parent_node
            path.append(current_node)
        return path

    def expand(self, state_space: StateSpace):
        successors: list[Node] = []
        children = state_space.successor(self.state)
        for child in children:
            s = Node(child, self, self.depth + 1)
            successors = insert(s, successors)
        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Depth: {self.depth}"


def insert(node: Node, queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """
    Returns a copy of the queue with the node inserted.
    Use insert_as_first=True for DFS, False for BFS.
    """
    if insert_as_first:
        return [node] + queue
    else:
        return queue + [node]


def insert_all(nodes_to_add: list[Node], queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """
    Inserts all nodes into the queue using insert().
    Returns a new list with the combined elements.
    """
    for node in nodes_to_add:
        queue = insert(node, queue, insert_as_first)
    return queue


def remove_first(queue: list[Node]) -> Node:
    """Removes and returns the first element from the queue."""
    return queue.pop(0)


class Searcher:
    def __init__(self, initial_state, goal_state, state_space: StateSpace = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space

    def tree_search(self, insert_as_first: bool = True) -> list[Node]:
        """
        Search the tree for the goal state and return the path from
        initial state to goal state using either DFS or BFS.
        """
        fringe: list[Node] = []
        initial_node = Node(self.initial_state)
        fringe = insert(initial_node, fringe, insert_as_first)
        while fringe:
            node = remove_first(fringe)
            if node.state == self.goal_state:
                return node.path()
            children = node.expand(self.state_space)
            fringe = insert_all(children, fringe, insert_as_first)
            print(f"Fringe: {fringe}")

    def run(self, insert_as_first: bool = True):
        path = self.tree_search(insert_as_first)
        print("Solution path:")
        for node in path:
            node.display()


if __name__ == '__main__':
    input_state_space = {
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

    searcher = Searcher('A', 'J', state_space=StateSpace(input_state_space))

    print("Depth-First Search:")
    searcher.run(insert_as_first=True)

    print("\nBreadth-First Search:")
    searcher.run(insert_as_first=False)
