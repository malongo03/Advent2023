
def load_graph(filename):
    '''
    Loads the tree from a file.

    Inputs:
      filename [str]: The name of the file to load the tree from.

    Returns [Tree]: The root of the tree or ``None`` if the file does
      not exist.
    '''
    with open(filename, encoding = "utf-8") as test_file:
        input_lines = test_file.read().split('\n')

    # Build graph
    nodes = {}
    for line in input_lines[2:]:
        node_id, _, child1, child2= line.split()
        nodes[node_id] = [child1[1:4], child2[0:3]]

    return input_lines[0], nodes

def fun_ction(file):
    instructions, graph = load_graph(file)

    node = "AAA"
    nodes = ["AAA"]
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


print(fun_ction("day_8.txt"))
