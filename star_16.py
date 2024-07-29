"""
Module to solve the second star of Day 8 of the Advent of Code 2023, which is
the 16th star overall.
"""

import math
def load_graph(filename):
    """
    Creates graph as an adjaceny dictionary from file, while also exporting the
    direction list and the list of nodes ending in A.

    Inputs:
      filename [str]: The name of the file to load the graph from.

    Returns:
        str
        dict{str: lst[str]}
        lst[str]
    """
    with open(filename, encoding = "utf-8") as file:
        input_lines = file.read().split('\n')

    # Build graph
    graph = {}
    a_nodes = []
    for line in input_lines[2:]:
        node_id, _, child1, child2= line.split()
        graph[node_id] = [child1[1:4], child2[0:3]]
        if node_id[2] == "A":
            a_nodes.append(node_id)

    return input_lines[0], graph, a_nodes

def follow_directions_simultanetously(file):
    """
    Takes in a list of left and right commands and a graph adjacency list
    (see Day 8 of Advent of Code 2023) and processes it to find how many turns
    it takes to go from every node ending in A to simultanetously end up at
    every node ending in Z. It does this by taking advantage of the looping
    cycles of each A to Z path and finding the least common multiplier of these
    cycles lengths.

    Inputs:
        file [str]: the input file name

    Returns int
    """
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


print(follow_directions_simultanetously("day_8.txt"))
