"""
Module to solve the first and second star of Day 11 of the Advent of Code 2023,
which are the 21st and 22nd stars overall.
"""
def expand_cols(galaxy_positions, width, expansion_rate):
    """
    Takes in a sequence of coordiantes for the positions of galaxies, and
    adjusts the coordinates to reflect the expansion of empty columns.

    Input:
        galaxy_positions [lst[tuple(int, int)]]: coordiantes for the positions
            of all of the galaxies.
        width [int]: the width of the initial data the galaxies were found in.
        expansion_rate [int]: how many extra columns of distance each empty
            column should be worth as compared to an occupied column.

    Returns lst[tuple(int, int)]
    """
    galaxy_positions.sort(key = lambda x: x[1])
    galaxy_number = len(galaxy_positions)
    new_galaxy_positions = []
    gal_index = 0
    expansion = 0
    for col_index in range(width):
        found_galaxy = False
        start_gal_index = None
        while gal_index < galaxy_number:
            _, gal_col = galaxy_positions[gal_index]
            if gal_col == col_index:
                found_galaxy = True
                if start_gal_index is None:
                    start_gal_index = gal_index
                gal_index += 1
            else:
                break
        if found_galaxy:
            for i in range(start_gal_index, gal_index):
                gal_row, gal_col = galaxy_positions[i]
                new_galaxy_positions.append((gal_row, gal_col + expansion))
        else:
            expansion += expansion_rate

    return new_galaxy_positions


def calculate_galactic_distances(file, expansion_rate = 1):
    """
    Taking in a map of the night sky and an expansion rate (see Day 11 of Advent
    of Code 2023) and calculates the sum of the Manhattan distances between all
    pairs of galaxies while accounting for the expansion of the universe over
    time.

    Inputs:
        file [str]: the name of the input file.
        expansion_rate [int = 1]: how many extra rows or cols of distance an
            unoccupied row or col should be worth respectively as compared to a
            row or column that has at least one galaxy found in it.

    Return int
    """
    with open(file, encoding = "utf-8") as f:
        star_map = [[*line] for line in f.read().split("\n")]

    galaxy_positions = []
    row_expansion = 0
    for row, line in enumerate(star_map):
        found_galaxies = False
        for col, cha in enumerate(line):
            if cha == "#":
                galaxy_positions.append((row + row_expansion, col))
                found_galaxies = True
        if not found_galaxies:
            row_expansion += expansion_rate

    galaxy_positions = expand_cols(galaxy_positions, len(star_map[0]), expansion_rate)

    answer = 0
    galaxy_number = len(galaxy_positions)
    for i in range(galaxy_number - 1):
        first_galaxy = galaxy_positions[i]
        for second_galaxy in galaxy_positions[i + 1:]:
            row_1, col_1 = first_galaxy
            row_2, col_2 = second_galaxy
            manhattan_distance = abs(row_1 - row_2) + abs(col_1 - col_2)
            answer += manhattan_distance

    return answer

print(calculate_galactic_distances("day_11.txt"))
print(calculate_galactic_distances("day_11.txt", 999999))
