"""
Module to solve the first star of Day 8 of the Advent of Code 2023, which is the
15th star overall.
"""
def load_graph(filename):
    """
    Creates graph as an adjaceny dictionary from file, while also exporting the
    direction list.

    Inputs:
      filename [str]: The name of the file to load the graph from.

    Returns:
        str
        dict[str: lst[str]]
    """
    with open(filename, encoding = "utf-8") as file:
        input_lines = file.read().split('\n')

    # Build graph
    nodes = {}
    for line in input_lines[2:]:
        node_id, _, child1, child2= line.split()
        nodes[node_id] = [child1[1:4], child2[0:3]]

    return input_lines[0], nodes

def follow_directions(file):
    """
    Takes in a list of left and right commands and a graph adjacency list
    (see Day 8 of Advent of Code 2023) and processes it to find how many turns
    it takes to go from node AAA to node ZZZ.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    instructions, graph = load_graph(file)

    node = "AAA"
    break_flag = True
    path_steps = 0
    while break_flag:
        for cha in instructions:
            if cha == "L":
                node = graph[node][0]
            else:
                node = graph[node][1]
            path_steps += 1
            if node == "ZZZ":
                break_flag = False
                break

    return path_steps


print(follow_directions("day_8.txt"))
