"""
Module to solve the first and second star of Day 12 of the Advent of Code 2023,
which are the 23rd and 24st stars overall.
"""
from functools import cache

@cache
def recurse_nonogram_row(row, numbers):
    """
    Finds the number of valid solutions to a nonogram (aka Picross) row using
    dynamic programming and the help of the functools cache function, which will
    remember rows and numbers we've already counted solutions for.

    Inputs:
        row [str]: a picross row consisting of "#" (filled tiles),
            "."(empty tiles), and "?" (unknown tiles).
        numbers [lst[int]]: a list of integers adhering to the traditional
            picross hints telling us what a valid solution to the row will look
            like.

    Returns int
    """

    if row == "":
        # If the row is empty, there can be no chucks that have to be placed or
        # else there are no valid solutions.
        if numbers == []:
            return 1
        return 0
    if numbers == []:
        # If numbers is empty, the row has to be full of empty tiles or else
        # there are no valid solutions.
        if "#" in row:
            return 0
        return 1

    if row[0] == ".":
        # Strips away any known to be empty tiles.
        return recurse_nonogram_row(row.lstrip("."), numbers)

    if row[0] == "?":
        # Two possible options here for this ?. Counts the number of valid
        # solutions if this ? is a . and adds them to the number of valid
        # solutions for if this ? is a #.
        first_possibility = recurse_nonogram_row(row[1:], numbers)
        second_possibility = recurse_nonogram_row("#" + row[1:], numbers)
        return first_possibility + second_possibility

    # Else row[0] == "#"
    # We know the next chunk has to start here, leading to the following checks:
    if "." in row[:numbers[0]]:
        # If there is an interruption that prohibits us from filling out the
        # the next chunk, we know this row to have no valid solutions
        return 0
    if row[numbers[0]] == "#":
        # If the chunk is too long, we know this row to have no valid solutions
        return 0
    # Otherwise, the placement of the next chunk is forced and we can move on.
    return recurse_nonogram_row(row[numbers[0] + 1:], numbers[1:])


def solve_nonogram_rows(file, duplication = 1):
    """
    Takes in a map of broken, working, and unknown springs (See Day 12 of the
    Advent of Code 2023) along with the number of bunches of broken springs per
    row, and calculates the sum of the possibilities for each row. It can also
    duplicate the size of each row in case the map happens to be folded.

    Input:
        file [str]: the filename of the input
        duplication [int = 1]: for each row, how duplicated should it be (with
            1 meaning no duplication, 2 meaning the row is doubled, etc.)

    Returns int
    """
    with open(file, encoding = "utf-8") as f:
        text = [(line.split()[0], line.split()[1]) for line in f.read().split("\n")]
        picross_rows = [(row, tuple(map(int, nums.split(",")))) for row, nums in text]

    total_arrangements = 0
    for index, row_w_num in enumerate(picross_rows):
        row, numbers = row_w_num
        new_row = "?".join([row] * duplication) + "."
        new_numbers = numbers * duplication
        total_arrangements += recurse_nonogram_row(new_row, new_numbers)
        print(f"Finished {index + 1} / {len(picross_rows)}!")

    return total_arrangements

print(solve_nonogram_rows("day_12.txt"))
print(solve_nonogram_rows("day_12.txt", 5))
