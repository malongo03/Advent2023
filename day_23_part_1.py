"""
Module to solve the first star of Day 23 of the Advent of Code 2023, which is
the 45th star overall.
"""
import sys

DIRECTIONS = (1, -1, 1j, -1j)
CHAR_DIRECTIONS = {"^": -1, "v": 1, ">": 1j, "<": -1j, ".": 0, "#": 0}

def find_start(node_type_dict):
    index = 0
    while True:
        if node_type_dict[complex(0, index)] == ".":
            return complex(0, index)
        index += 1


def find_nodes(filename):
    with open(filename, encoding = "utf-8") as f:
        text = f.read().strip().split()
        height = len(text)
        node_type_dict = {complex(row, col): char
                          for row, line in enumerate(text)
                          for col, char in enumerate(line)}

    start_node = find_start(node_type_dict)
    adjacency_list = {start_node: []}
    queue = [(start_node, start_node + 1, 1)]
    visited = {start_node}

    while queue:
        source_node, current_node, curr_direction = queue.pop()
        current_char = "."
        length = 1
        exit_node_flag = False

        # Find next node
        while current_char == "." and not exit_node_flag:
            curr_direction = [direction for direction in DIRECTIONS if
                              direction != -curr_direction and
                              node_type_dict[current_node + direction] != "#"][0]
            current_node += curr_direction
            current_char = node_type_dict[current_node]
            length += 1

            # Check for ending node
            if current_node.real == height - 1:
                exit_node_flag = True

        # Case for ending node
        if exit_node_flag:
            exit_node = current_node
            adjacency_list[source_node] = adjacency_list.get(source_node, []) + \
                                          [(exit_node, length)]
            continue

        #
        last_direction = CHAR_DIRECTIONS[current_char]
        current_node += last_direction
        length += 1
        adjacency_list[source_node] = adjacency_list.get(source_node, []) + \
                                      [(current_node, length)]

        # Add new items to queue if necessary
        if current_node not in visited:
            visited.add(current_node)


            next_directions = (direction for direction in DIRECTIONS if
                               direction == CHAR_DIRECTIONS[node_type_dict[current_node + direction]])
            for next_direction in next_directions:
                target_node = current_node + next_direction
                queue.append((current_node, target_node, next_direction))

    return adjacency_list, start_node, exit_node


def find_topological_order(adjacency_list, start_node, exit_node):
    incoming_edges = {}
    for source, targets in adjacency_list.items():
        for target, _ in targets:
            incoming_edges[target] = incoming_edges.get(target, set()).union({source})

    queue = {start_node}
    topo_order = []
    while queue:
        source = queue.pop()
        topo_order.append(source)
        if source == exit_node:
            continue
        for target, _ in adjacency_list[source]:
            incoming_edges[target].remove(source)
            if not incoming_edges[target]:
                queue.add(target)

    return topo_order


def find_longest_path(topo_order, adjacency_list, start_node, exit_node):
    costs = {node: float("inf") for node in topo_order}
    costs[start_node] = 0

    for source in topo_order:
        if source == exit_node:
            continue
        for target, cost in adjacency_list[source]:
            if costs[source] - cost < costs[target]:
                costs[target] = costs[source] - cost

    return -costs[exit_node]


def star_45(filename):
    adjacency_list, start_node, exit_node = find_nodes(filename)
    topo_order = find_topological_order(adjacency_list, start_node, exit_node)
    longest_path = find_longest_path(topo_order, adjacency_list, start_node, exit_node)
    return longest_path


print(star_45(sys.argv[1]))
