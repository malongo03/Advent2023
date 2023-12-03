"""
Module to solve the first star of Day 3 of the Advent of Code 2023, which is the
5th star overall.
"""
SYMBOLS = ["@", "#", "$", "%", "&", "*", "-", "+", "=", "/"]

def find_symbols(matrix):
    """
    Takes in a matrix, and returns a list of coordinates for every symbol in the
    matrix.

    Inputs:
        file(str): the name of the input file

    Returns list[tuple(int, int)]
    """
    output = []
    for i, line in enumerate(matrix):
        for j, dot in enumerate(line):
            if dot in SYMBOLS:
                output.append((i, j))
    return output


def is_adjacent(row, start_col, end_col, sym_coor):
    """
    Takes in a number's position in a matrix and checks if it is adjacent to any
    symbols in the matrix.

    Inputs:
        row(int): the row coordinate of the number
        start_col(int): the starting column coordinate of a number
        end_col(int): the ending column coordinate of a number
        gear_coor(list[tuple(int, int)]: a list of coordinates for symbols in
            the matrix

    Returns bool
    """
    for i, j in sym_coor:
        if (row - 1 <= i <= row + 1) and (start_col - 1 <= j <= end_col + 1):
            return True
    return False


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


def find_part_numbers(file):
    """
    Takes in an engine schematic (see Day 3 of Advent of Code 2023), and
    returns the sum of every engine part in the schematic (i.e., every number in
    the matrix that is adjacent to a symbol).

    My solution passes through the schematic twice. Once to find symbols, and a
    second time to find adjacent numbers.

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """
    # Convert input into format which can be treated as a matrix
    f = open(file, encoding = "utf-8")
    matrix = f.read()
    matrix = matrix.split("\n")

    # Find all symbols in the matrix
    sym_coor = find_symbols(matrix)


    # Find all numbers adjacent to a symbol and add them to the answer
    answer = 0
    for row, line in enumerate(matrix):
        end_col = -1
        for col, dot in enumerate(line):
            if dot.isdigit() and col > end_col:
                start_col = col
                number, end_col = find_number(start_col, line)
                if is_adjacent(row, start_col, end_col, sym_coor):
                    answer += number

    return answer


print(find_part_numbers("day_3.txt"))
