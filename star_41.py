MOVEMENTS = (1j, 1, -1j, -1)
def parse_input(filename):
    with open(filename, encoding = "utf-8") as f:
        array = [[*line] for line in f.read().split()]
    height  = len(array)
    width = len(array[0])
    return array, height, width


def find_S(array):
    for row, line in enumerate(array):
        for col, char in enumerate(line):
            if char == "S":
                return complex(row, col)


def print_output(array, visited):
    change_tile = visited.union(set())
    while change_tile:
        space = change_tile.pop()
        array[int(space.real)][int(space.imag)] = "O"
    with open("output.txt", "w", encoding = "utf-8") as f:
        array = ["".join(line) for line in array]
        text = "\n".join(array)
        f.write(text)


def walk_the_walk(filename, steps):
    def find_neighbors(space):
        pseudo_neigh = set()
        neighbors = set()
        for delta in MOVEMENTS:
            new_space = space + delta
            if 0 <= new_space.real < height and 0 <= new_space.imag < width and \
            array[int(new_space.real)][int(new_space.imag)] == ".":
                pseudo_neigh.add(new_space)
        for pseduo_space in pseudo_neigh:
            for delta in MOVEMENTS:
                new_space = pseduo_space + delta
                if new_space not in visited and \
                array[int(new_space.real)][int(new_space.imag)] != "#":
                    neighbors.add(new_space)
        return neighbors

    array, height, width = parse_input(filename)
    source = find_S(array)
    queue = {source}
    new_queue = set()
    visited = queue.copy()

    for _ in range(steps // 2):
        while queue:
            space = queue.pop()
            new_queue = new_queue.union(find_neighbors(space))
        visited = visited.union(new_queue)
        queue = new_queue.union(set())
        new_queue = set()

    # print_output(array, visited)
    return len(visited)


print(walk_the_walk("day_21.txt", 65))