"""
Module to solve the first and second star of Day 14 of the Advent of Code 2023,
which are the 27th and 28th stars overall.
"""
def tilt_direction(matrix, direction):
    """
    Simuates a tilt of a matrix of immovable square rocks "#" and movable round
    rocks "O" in one of four cardinal directions.

    Inputs:
        matrix [lst[str]]: a list of strings representing a field of square and
            round rocks.
        direction [cha]: a character representing the direction of the tilt.

    Returns lst[str]
    """
    # Determines paramaters of function based on the direction of the tilting.
    direction_dict = {"N": (True, True),
                      "S": (False, True),
                      "W": (True, False),
                      "E": (False, False)}
    is_reversed, needs_transpose = direction_dict[direction]

    if needs_transpose:
        matrix = ["".join([line[i] for line in matrix])
                  for i in range(len(matrix[0]))]

    # Tilts each row by spliting it along the square blocks, sorting the
    # segments in the appropiate order, and then joining them together again.
    new_matrix = []
    for line in matrix:
        sorted_lines = ["".join(sorted(subline, reverse = is_reversed))
                        for subline in line.split("#")]
        new_line = "#".join(sorted_lines)
        new_matrix.append(new_line)

    if needs_transpose:
        new_matrix = ["".join([line[i] for line in new_matrix])
                      for i in range(len(new_matrix[0]))]

    return new_matrix


def rock_washing_machine(filename):
    """
    A function to take in a map of a movable platform of round and square rocks
    (See Day 14 of the Advent of Code 2023) and prints the load on the north
    support after tilting it to the north once, and the load after tilting it
    in a cycle of north, west, south, and east 1,000,000,000 times.

    Input:
        filename [str]: the filename of the input map represented as a matrix.
    """
    with open(filename, encoding = "utf-8") as f:
        # We will be keeping the matrix as composed of a list of strings to take
        # advantage of python's built in sorting algorithms
        matrix = f.read().split("\n")

    # Part 1
    # Tilts matrix north and then calculates the load on the north support.
    part_1_matrix = tilt_direction(matrix, "N")
    answer = 0
    for row_index, row in enumerate(reversed(part_1_matrix)):
        for space in row:
            if space == "O":
                answer += row_index + 1
    print(f"The answer to Star 27 is {answer}")

    # Part 2
    # Tilts the matrix in a cycle of North, West, South, and East, storing the
    # results so it can find a loop. Once it has found a loop, it determines
    # which element in the loop corrosponds to the result of 1,000,000,000
    # cycles.
    DIRECTIONS = ["N", "W", "S", "E"]
    find_loop = []
    loop = True
    while loop:
        find_loop.append(matrix)
        for direction in DIRECTIONS:
            matrix = tilt_direction(matrix, direction)
        for index, comp_matrix in enumerate(find_loop):
            if matrix == comp_matrix:
                loop_start = index
                loop = False
                break
    loop_length = len(find_loop) - loop_start
    index = (1000000000 - loop_start) % (loop_length) + loop_start
    matrix = find_loop[index]

    answer = 0
    for row_index, row in enumerate(reversed(matrix)):
        for space in row:
            if space == "O":
                answer += row_index + 1

    print(f"The answer to Star 28 is {answer}.")

rock_washing_machine("day_14.txt")
