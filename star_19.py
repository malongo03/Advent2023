"""
Module to solve the first star of Day 10 of the Advent of Code 2023, which is
the 19th star overall.
"""
def find_loop_trail(pipe_map):
    """
    Takes in a map of pipes, finds the location of the starting tile and one of
    the tiles it is connected to. It also finds the direction this connecting
    tile is approached from.

    Input:
        pipe_map [lst[lst[cha]]]

    Returns:
        (int, int): the corrdinate of tile connecting to S (i.e., the start of
            loop)
        cha: the direction of S relative to the connecting tile
    """
    break_flag = False
    for row, line in enumerate(pipe_map):
        for col, char in enumerate(line):
            if char == "S":
                break_flag = True
                start_row = row
                start_col = col
                break
        if break_flag:
            break
    DIRECTIONS = [("N", 1, 0), ("E", 0, -1), ("S", 1, 0), ("W", 0, 1)]
    height = len(pipe_map)
    width = len(pipe_map[0])

    for from_direction, diff_row, diff_col in DIRECTIONS:
        trail_row = start_row + diff_row
        trail_col = start_col + diff_col
        if (0 <= trail_row < height) and (0 <= trail_col < width):
            trail_char = pipe_map[trail_row][trail_col]
            match (from_direction, trail_char):
                case ("N", "|") | ("N", "L") | ("N", "J"):
                    return (trail_row, trail_col), from_direction
                case ("E", "-") | ("E", "L") | ("E", "F"):
                    return (trail_row, trail_col), from_direction
                case ("S", "|") | ("S", "7") | ("S", "F"):
                    return (trail_row, trail_col), from_direction
                case ("W", "-") | ("W", "7") | ("W", "J"):
                    return (trail_row, trail_col), from_direction


def track_loop(loop_tile, st_from_direction, pipe_map):
    """
    Traces a loop through a pipe map using the start of the loop and the
    direction it shouldn't head in (i.e., the direction from which this tile
    was arrived at).

    Inputs:
        loop_tile [tuple(int, int)]: the coordinates of the start of the loop
        st_from_direction [cha]:
        pipe_map [lst[lst[cha]]]: the matrix of pipes representing the map

    Returns:
        lst[tuple(int, int)]: a list of cooridantes that the loop visited
    """
    pipe_row, pipe_col = loop_tile

    loop = [(pipe_row, pipe_col)]
    pipe_char = pipe_map[pipe_row][pipe_col]
    from_direction = st_from_direction
    while True:
        match pipe_char:
            case "|":
                if from_direction == "N":
                    pipe_row += 1
                    # pipe_col += 0
                    # from_direction = "N"
                else:
                    pipe_row += -1
                    # pipe_col += 0
                    # from_direction = "S"
            case "-":
                if from_direction == "W":
                    # pipe_row += 0
                    pipe_col += 1
                    # from_direction = "W"
                else:
                    # pipe_row += 0
                    pipe_col += -1
                    # from_direction = "E"
            case "L":
                if from_direction == "N":
                    # pipe_row += 0
                    pipe_col += 1
                    from_direction = "W"
                else:
                    pipe_row += -1
                    # pipe_col += 0
                    from_direction = "S"
            case "J":
                if from_direction == "N":
                    # pipe_row += 0
                    pipe_col += -1
                    from_direction = "E"
                else:
                    pipe_row += -1
                    # pipe_col += 0
                    from_direction = "S"
            case "7":
                if from_direction == "S":
                    # pipe_row += 0
                    pipe_col += -1
                    from_direction = "E"
                else:
                    pipe_row += 1
                    # pipe_col += 0
                    from_direction = "N"
            case "F":
                if from_direction == "S":
                    # pipe_row += 0
                    pipe_col += 1
                    from_direction = "W"
                else:
                    pipe_row += 1
                    # pipe_col += 0
                    from_direction = "N"
            case "S":
                break
        pipe_char = pipe_map[pipe_row][pipe_col]
        loop.append((pipe_row, pipe_col))

    return loop


def find_beetle_loop_length(file):
    """
    Takes in a map of a field of pipes that a beetle-like organism has entered
    (see Day 10 of the Advent of Code 2023) and finds the length of the
    pipe loop that the beetle is scurring in.

    Inputs:
        file [str]: the filename of the input

    Returns int
    """
    with open(file, encoding = "utf-8") as f:
        pipe_map = [[*line] for line in f.read().split("\n")]

    loop_tile, from_direction = find_loop_trail(pipe_map)

    loop_length = len(track_loop(loop_tile, from_direction, pipe_map))

    return loop_length


print(find_beetle_loop_length("day_10.txt") // 2)
