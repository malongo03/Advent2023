"""
Module to solve the first star of Day 25 of the Advent of Code 2023,
which is the 49th star overall. (The 50th star is granted for free upon the
completion of the other 49 stars)
"""
import sys
import random

class Node:
    """
    A simple class to represent a node in a graph, storing pointers to the nodes
    it has edges to.

    Hashable to allow for its placement in dictionaries and sets. It has a
    function to merge a node's size and edges into itself.
    """

    # This parameter keeps track of how many
    size: int
    name: str
    edges: dict["Node", int]

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.edges = {}

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name and type(self.name) is type(other.name)

    def __repr__(self):
        return f"Node({self.name}, {self.size})"

    @property
    def weight(self) -> int:
        return sum(self.edges.values())

    def merge_node_into(self, other: "Node"):
        self.size += other.size

        for node, weight in other.edges.items():
            if node == self:
                self.edges.pop(other)
                continue

            new_weight = self.edges.get(node, 0) + weight
            self.edges[node] = new_weight
            node.edges[self] = new_weight
            node.edges.pop(other)


def copy_graph(og_graph: set[Node]) -> set[Node]:
    """
    A function to copy my set of connected nodes. This is necessary
    because deepcopy gets stuck in a recursion loop, as the nodes all link to
    each other. Recursion is avoided by using a new graph dictionary as a
    reference to check whether a node has already been created.
    """
    new_graph = {}

    for old_node in og_graph:
        if old_node.name not in new_graph:
            new_graph[old_node.name] = Node(old_node.name, old_node.size)
        new_node = new_graph[old_node.name]

        for old_neighbor, weight in old_node.edges.items():
            if old_neighbor.name not in new_graph:
                new_graph[old_neighbor.name] = Node(old_neighbor.name, new_node.size)
            new_neighbor = new_graph[old_neighbor.name]
            new_node.edges[new_neighbor] = weight

    return set(new_graph.values())


def create_graph(edge_list: list[tuple[str, list[str]]]) -> set[Node]:
    """
    Creates a graph from the parsed Advent of Code data.
    """

    graph = {}

    for source, neighbors in edge_list:
        if source not in graph:
            graph[source] = Node(source, 1)
        source_node = graph[source]

        for target in neighbors:
            if target not in graph:
                graph[target] = Node(target, 1)
            target_node = graph[target]

            source_node.edges[target_node] = 1
            target_node.edges[source_node] = 1

    return set(graph.values())


def search_for_cut_size(og_graph: set[Node], cut_size: int) -> tuple[int, int]:
    """
    This function is unfortunately probabilistic. A more systematic approach
    was attempted, but was unacceptably slow. Instead, we can rely on the
    graph's size in comparison to the small cut we need find.

    This function should succeed within a few cycles.
    """
    total_size = len(og_graph)
    node_list: list[Node] = list(og_graph)

    while True:
        graph = copy_graph(og_graph)

        rand_index = random.randrange(total_size)
        a_node = node_list[rand_index]
        graph.remove(a_node)

        while len(graph) > 0:
            weight: int = a_node.weight
            if weight == cut_size:
                return a_node.size, total_size - a_node.size

            sorted_edges = sorted(a_node.edges.items(), key=lambda x: x[1], reverse=True)
            next_merge = sorted_edges[0][0]

            a_node.merge_node_into(next_merge)
            graph.remove(next_merge)


def parse_input(filename: str) -> list[tuple[str, list[str]]]:
    """
    Reads in a day 25 Advent of Code text file and parses it. The input
    specifications can be found the Advent of Code website.

    The output specifications are the following format:
    [
    (source, [neighbor1, neighbor2, ...]),
    ...]
    """

    with open(filename, 'r', encoding='utf-8') as f:
        raw_lines = f.read().strip().split('\n')
    edge_list: list[tuple[str, list[str]]] = []
    for line in raw_lines:
        node, neighbors = line.split(":")
        neighbors = neighbors.split()
        edge_list.append((node, neighbors))

    return edge_list


def main(filename: str) -> None:
    random.seed()
    graph = create_graph(parse_input(filename))
    size1, size2 = search_for_cut_size(graph, 3)
    print(f"Your answer to Day 25 is {size1 * size2}")


if __name__ == '__main__':
    main("day_25.txt")
    sys.exit(0)
