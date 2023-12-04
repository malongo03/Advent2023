"""
Module to solve the second star of Day 3 of the Advent of Code 2023, which is the
6th star overall.
"""

def find_number(col, line):
    """
    Takes in a number's starting column in a line and finds the column it ends,
    along with the value of the number.

    Inputs:
        col(int): the column coordinate of the start of a number
        line(str): the line of the matrix that the number was found in

    Returns int, int
    """
    number = 0
    while True:
        pot_digit = line[col]
        if pot_digit.isdigit():
            number = number * 10 + int(pot_digit)
            col += 1
            if col > 139:
                break
        else:
            break

    return number, col - 1


def find_gear_ratios(file):
    """
    Takes in an engine schematic (see Day 3 of Advent of Code 2023), finds the
    gears (every "*" symbol with two adjacent number), calculates the gear
    ratio (the product of these numbers), and then sums the ratios of the entire
    schematic.

    This newer solution passes through the schematic once.

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """
    # Convert input into format which can be treated as a matrix
    f = open(file, encoding = "utf-8")
    matrix = f.read()
    matrix = matrix.split("\n")

    # Find all potential gears and put their coordinates as keys to a
    # dictionary, and find all numbers and add their coordinates to a list.
    num_coor = []
    gear_coor = {}
    for row, line in enumerate(matrix):
        end_col = -1
        for col, dot in enumerate(line):
            if col <= end_col:
                pass
            elif dot == "*":
                gear_coor[(row, col)] = []
            elif dot.isdigit():
                start_col = col
                number, end_col = find_number(start_col, line)
                num_coor.append((row, start_col, end_col, number))

    # Find numbers adjacent to a potential gear and add them to the adjaceny
    # list of the gears
    for row, start_col, end_col, number in num_coor:
        for i, j in gear_coor.keys():
            if (row - 1 <= i <= row + 1) and (start_col - 1 <= j <= end_col + 1):
                gear_coor[(i, j)] = gear_coor[(i, j)] + [number]
                break

    # Find which potential gears are true gears and add gear ratios to answer
    answer = 0
    for adj_nums in gear_coor.values():
        if len(adj_nums) == 2:
            answer += adj_nums[0] * adj_nums[1]

    return answer


print(find_gear_ratios("day_3.txt"))
