"""
Module to solve Day 18 of the Advent of Code 2023, which are the 35th and 36th
stars overall.
"""

# A dictionary to translate direction commands into their complex counterparts.
DIRECTIONS = {"R": 1j, "D": 1, "L": -1j, "U": -1,
              "0": 1j, "1": 1, "2": -1j, "3": -1}

def find_lagoon_area(dig_instructions):
    """
    Calculates the area of the lagoon by following the dig instructions to find
    the vertices, then applying the shoelace formula and Pick's Theorem.

    Inputs:
        dig_instructions [lst[tuple(str, int)]]: the instructions for digging
            the border of the lava lagoon, consisting of a direction string and
            a length.

    Returns int
    """
    verts = []
    border = 0
    current_pos = 0j

    # Follows dig instructions, storing the vertix tiles created by each
    # instruction and the number of tiles dug along the border.
    for direction, move_len in dig_instructions:
        move = DIRECTIONS[direction]
        current_pos += move * move_len
        verts.append(current_pos)
        border += move_len

    verts = [(int(z.real), int(z.imag)) for z in verts]
    vert_num = len(verts)
    # To ensure vert_{vert_num} = vert_{0} for shoelace formula
    verts.append(verts[0])

    # Applies the shoelace area formula to the vertices of the lagoon lake, or
    # rather, the coordinate of the upper-left corner of each of the vertix
    # tiles. This distinction is important, and it's why we have to then use
    # Pick's theorem to correct the discrepency).
    shoelace = 0
    for i in range(vert_num):
        shoelace += (verts[i][0] * verts[i + 1][1]) - (verts[i][1] * verts[i + 1][0])
    shoelace = abs(shoelace // 2)

    # Uses Picks's theorem to account for the border tiles of the lagoon lake
    # that were missed by the shoelace calculation.
    answer = shoelace + border // 2 + 1

    return answer

def solve_day_18(filename):
    """
    Parses the inputs for Day 17 of the Advent of Code 2023, spliting them into
    inputs for the first star solution and the second star solution. It then
    prints the results of passing these inputs to the lagoon lake area solver.

    Input:
        filename [str]: the filename of the input.
    """
    with open(filename, encoding = "utf-8") as f:
        dig_instructions = [line.split() for line in f.read().split("\n")]
        star_1_instructions = [(direct, int(dig_len))
                            for direct, dig_len, _ in dig_instructions]
        star_2_instructions = [(code[-2], int(code[2: -2], 16))
                            for _, _, code in dig_instructions]
    print(f"The answer to Star 35 is {find_lagoon_area(star_1_instructions)}.")
    print(f"The answer to Star 36 is {find_lagoon_area(star_2_instructions)}.")

if __name__ == "__main__":
    solve_day_18("day_18.txt")
