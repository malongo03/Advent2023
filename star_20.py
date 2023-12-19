"""
Module to solve the second star of Day 10 of the Advent of Code 2023, which is
the 20th star overall.
"""
def find_loop_trail(pipe_map):
    """
    Takes in a map of pipes, finds the locations of the starting tile and one of
    the tiles it is connected to. It also finds the direction this connecting
    tile is approached from.

    Input:
        pipe_map [lst[lst[cha]]]

    Returns:
        (int, int): the coordiates of the S tile
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
                    return (start_row, start_col), (trail_row, trail_col), from_direction
                case ("E", "-") | ("E", "L") | ("E", "F"):
                    return (start_row, start_col), (trail_row, trail_col), from_direction
                case ("S", "|") | ("S", "7") | ("S", "F"):
                    return (start_row, start_col), (trail_row, trail_col), from_direction
                case ("W", "-") | ("W", "7") | ("W", "J"):
                    return (start_row, start_col), (trail_row, trail_col), from_direction


def track_loop(loop_tile, st_from_direction, pipe_map):
    """
    Traces a loop through a pipe map using the start of the loop and the
    direction it shouldn't head in (i.e., the direction from which this tile
    was arrived at).

    Inputs:
        loop_tile [tuple(int, int)]: the coordinates of the start of the loop.
        st_from_direction [cha]: the position of the "S" tile relative to
            beginning of the loop.
        pipe_map [lst[lst[cha]]]: the matrix of pipes representing the map.

    Returns:
        lst[lst[bool]]: a matrix corrosponding with the pipe map that tracked
            which tiles the loop visited.
        cha: the direction from which the end of the loop (i.e., the S tile) was
            visited from.
    """
    pipe_row, pipe_col = loop_tile

    # Creates a matrix of booleans that represent whether a tile is part of the
    # boundary
    height = len(pipe_map)
    width = len(pipe_map[0])
    boundary_tiles = [[False for _ in range(width)] for _ in range(height)]
    boundary_tiles[pipe_row][pipe_col] = True

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
        boundary_tiles[pipe_row][pipe_col] = True

    return boundary_tiles, from_direction


def adjust_s(from_direction, to_direction):
    """
    Finds the type of pipe that the S tile is.

    Inputs:
        from_direction: the direction that the S tile approaches the first tile
            of the loop from.
        to_direction: the direction that the second-to-last tile of the loop
            approaches S from.

    Returns cha
    """
    to_direction = [to_direction]
    # Inverts the from_direction to find the location of the first tile of the
    # loop relative to S.
    match from_direction:
        case "S":
            to_direction.append("N")
        case "N":
            to_direction.append("S")
        case "E":
            to_direction.append("W")
        case "W":
            to_direction.append("E")

    # Uses the relative locations of the tiles that S is connected to determine
    # its shape.
    match to_direction:
        case ["N", "S"] | ["S", "N"]:
            return "|"
        case ["E", "W"] | ["W", "E"]:
            return "-"
        case ["N", "E"] | ["E", "N"]:
            return "L"
        case ["N", "W"] | ["W", "N"]:
            return "J"
        case ["S", "W"] | ["W", "S"]:
            return "7"
        case ["S", "E"] | ["E", "S"]:
            return "F"


def find_beetle_loop_area(file):
    """
    Takes in a map of a field of pipes that a rat-like organism has entered (see
    Day 10 of the Advent of Code 2023) and finds the discrete area of tiles
    enclosed by the loop of pipes the rat entered.

    Inputs:
        file [str]: the filename of the input

    Returns int
    """
    with open(file, encoding = "utf-8") as f:
        pipe_map = [[*line] for line in f.read().split("\n")]

    s_tile, loop_tile, from_direction = find_loop_trail(pipe_map)

    boundary_tiles, to_direction = track_loop(loop_tile, from_direction, pipe_map)

    start_row, start_col = s_tile
    pipe_map[start_row][start_col] = adjust_s(from_direction, to_direction)

    # Casts a ray through every row of the pipe map, determining whether each
    # tile of the row is enclosed by the loop of pipes using the point in
    # polygon raycasting method.
    answer = 0
    for row, line in enumerate(pipe_map):
        in_polygon = False
        for col, cha in enumerate(line):
            if boundary_tiles[row][col]:
                if cha in ["|", "L", "J"]:
                    in_polygon = not in_polygon
            elif in_polygon:
                answer += 1

    return answer


print(find_beetle_loop_area("day_10.txt"))
