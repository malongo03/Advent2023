def find_start(node_type_dict):
    index = 0
    while True:
        if node_type_dict[complex(0, index)] == ".":
            return complex(0, index)
        index += 1

DIRECTIONS = (1, -1, 1j, -1j)
CHAR_DIRECTIONS = {"^": -1, "v": 1, ">": 1j, "<": -1j, ".": 0, "#": 0}
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
            adjacency_list[exit_node] = adjacency_list.get(exit_node, []) + \
                                          [(source_node, length)]
            continue

        #
        last_direction = CHAR_DIRECTIONS[current_char]
        current_node += last_direction
        length += 1
        adjacency_list[source_node] = adjacency_list.get(source_node, []) + \
                                      [(current_node, length)]
        adjacency_list[current_node] = adjacency_list.get(current_node, []) + \
                                       [(source_node, length)]

        # Add new items to queue if neccessary
        if current_node not in visited:
            visited.add(current_node)


            next_directions = (direction for direction in DIRECTIONS if
                               direction == CHAR_DIRECTIONS[node_type_dict[current_node + direction]])
            for next_direction in next_directions:
                target_node = current_node + next_direction
                queue.append((current_node, target_node, next_direction))

    return adjacency_list, start_node, exit_node



def star_45(filename):
    adjacency_list, start_node, exit_node = find_nodes(filename)

    def find_longest_path(exit_node, source, visited):
        if source == exit_node:
            return 0
        edges = [(target, cost) for target, cost in adjacency_list[source]
                if target not in visited]
        if not edges:
            return None

        answer = 0
        for target, cost in edges:
            calulation = find_longest_path(exit_node, target,
                                           visited.union(frozenset({source})))
            if calulation is not None and calulation + cost > answer:
                answer = calulation + cost

        return answer

    return find_longest_path(exit_node, start_node, frozenset({start_node}))


print(star_45("day_23.txt"))