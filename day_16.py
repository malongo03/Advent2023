"""
Module to solve the first and second star of Day 15 of the Advent of Code 2023,
which are the 31st and 32nd stars overall.
"""
import sys

def energize_mirror(start_space, start_direct, mirror_dict):
    """
    Given a starting position, direction, and a field of mirrors, the function
    traces the path a light beam travels through the mirror, returning the set
    of tiles that it visits.

    Each position and direction is represented as a complex number. The real
    part is the row, while the imaginary part is the column.

    Inputs:
        start_space [Complex]: the starting position of the light beam.
        start_direct [Complex]: the starting direction of the light beam.
        mirror_dict [dict{Complex: str}]: the field of mirror the light travels
            through, represented as a dictionary.

    Returns set(Complex)
    """
    visited_w_direct = set()
    visited = set()
    stack = {(start_space - start_direct, start_direct)}

    # A depth first search of the mirror field by treating it as a graph.
    while stack:
        space, direction = stack.pop()
        space += direction
        if (space, direction) in visited_w_direct:
            continue
        match mirror_dict.get(space):
            case "/": stack.add((space, -complex(direction.imag, direction.real)))
            case "\\": stack.add((space, complex(direction.imag, direction.real)))
            case "|":
                if direction == 1j or direction == -1j:
                    stack.add((space, 1))
                    stack.add((space, -1))
                else: stack.add((space, direction))
            case "-":
                if direction == 1 or direction == -1:
                    stack.add((space, 1j))
                    stack.add((space, -1j))
                else: stack.add((space, direction))
            case ".": stack.add((space, direction))
            case None: continue
        # We do this last so that we have a chance to check for an invalid
        # position with the switch statement.
        visited.add(space)
        visited_w_direct.add((space, direction))
    return visited


def count_energized_tiles(filename):
    """
    Prints the maximum number of tiles that can be energized with the current
    lava generator's arrangement of mirrors (see Day 16 of Advent of Code 2023).

    Input:
        filename [str]: the filename of the input

    """
    with open(filename, encoding = "utf-8") as f:
        text = f.read().split()
    width = len(text[0])
    height = len(text)
    mirror_dict = {row + col * 1j: space
                   for row, line in enumerate(text)
                   for col, space in enumerate(line)}

    # Part 1
    energy = len(energize_mirror(0, 1j, mirror_dict))
    print(f"The answer to Star 31 is {energy}.")

    # Part 2
    max_energy = []
    for index in range(width):
        max_energy.append(len(energize_mirror(index * 1j, 1, mirror_dict)))
        max_energy.append(len(energize_mirror(index * 1j + height - 1, -1, mirror_dict)))
    for index in range(height):
        max_energy.append(len(energize_mirror(index, 1j, mirror_dict)))
        max_energy.append(len(energize_mirror(index + width * 1j - 1j, -1j, mirror_dict)))
    print(f"The answer to Star 32 is {max(max_energy)}.")


count_energized_tiles(sys.argv[1])
