import math
def load_graph(filename):
    """
    Creates graph as an adjaceny dictionary from file

    Inputs:
      filename [str]: The name of the file to load the graph from.

    Returns dict[int: lst[int]]
    """
    with open(filename, encoding = "utf-8") as test_file:
        input_lines = test_file.read().split('\n')

    # Build graph
    graph = {}
    a_nodes = []
    for line in input_lines[2:]:
        node_id, _, child1, child2= line.split()
        graph[node_id] = [child1[1:4], child2[0:3]]
        if node_id[2] == "A":
            a_nodes.append(node_id)

    return input_lines[0], graph, a_nodes

def fun_ction(file):
    instructions, graph, nodes = load_graph(file)

    path_steps = 0
    loop_number = [None for _ in range(len(nodes))]

    for index, start in enumerate(nodes):
        loop = True
        path_steps = 0
        node = start
        while loop:
            for cha in instructions:
                if cha == "L":
                    node = graph[node][0]
                else:
                    node = graph[node][1]
                path_steps += 1
                if node[2] == "Z":
                    loop_number[index] = path_steps
                    loop = False
                    break

    answer = loop_number[0]
    for loop_len in loop_number[1:]:
        answer = math.lcm(answer, loop_len)

    return answer


print(fun_ction("day_8.txt"))
