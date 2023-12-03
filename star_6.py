"""
Module to solve the second star of Day 3 of the Advent of Code 2023, which is the
6th star overall.
"""

def find_pot_gears(matrix):
    """
    Takes in a matrix, and prepares a dictionary where every key is the
    coordinates to a potential gear. These keys link to empty lists that can
    contain adjacent numbers.

    Inputs:
        matrix(lst[str]): the matrix of characters

    Returns dict{tuple(int, int): lst}
    """
    gear_coor = {}
    for i, line in enumerate(matrix):
        for j, dot in enumerate(line):
            if dot == "*":
                gear_coor[(i, j)] = []
    return gear_coor


def is_adjacent(number, row, start_col, end_col, gear_coor):
    """
    Take in a number and its position in a matrix and searches a dictionary of
    potential gears, adding itself to adjacency list of any potential gears it
    is adjacent to.

    Inputs:
        row(int): the row coordinate of the number
        start_col(int): the starting column coordinate of a number
        end_col(int): the ending column coordinate of a number
        gear_coor(dict{tuple(int, int): lst}): the dictionary of potential gears
            and their list of adjacent numbers.

    Returns dict{tuple(int, int): lst}
    """
    for sym in gear_coor:
        i, j = sym
        if (row - 1 <= i <= row + 1) and (start_col - 1 <= j <= end_col + 1):
            gear_coor[sym] = gear_coor[sym] + [number]

    return gear_coor


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

    My solution passes through the schematic twice. Once to find potential
    gears, and a second time to find the numbers adjacent to them.

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """
    # Convert input into format which can be treated as a matrix
    f = open(file, encoding = "utf-8")
    matrix = f.read()
    matrix = matrix.split("\n")

    # Find all potential gears and put them as keys to a dictionary
    gear_coor = find_pot_gears(matrix)

    # Find all numbers adjacent to a potential gear and adds them to the
    # corresponding adjacency lists.
    for row, line in enumerate(matrix):
        end_col = -1
        for col, dot in enumerate(line):
            if dot.isdigit() and col > end_col:
                start_col = col
                number, end_col = find_number(start_col, line)
                gear_coor = is_adjacent(number, row, start_col, end_col, gear_coor)

    # Find which potential gears are true gears and add gear ratios to answer
    answer = 0
    for adj_nums in gear_coor.values():
        if len(adj_nums) == 2:
            answer += adj_nums[0] * adj_nums[1]

    return answer


print(find_gear_ratios("day_3.txt"))
