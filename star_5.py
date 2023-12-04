"""
Module to solve the first star of Day 3 of the Advent of Code 2023, which is the
5th star overall.
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
        potential_digit = line[col]
        if potential_digit.isdigit():
            number = number * 10 + int(potential_digit)
            col += 1
            if col > 139:
                break
        else:
            break

    return number, col - 1


SYMBOLS = ["@", "#", "$", "%", "&", "*", "-", "+", "=", "/"]
def find_part_numbers(file):
    """
    Takes in an engine schematic (see Day 3 of Advent of Code 2023), and
    returns the sum of every engine part in the schematic (i.e., every number in
    the matrix that is adjacent to a symbol).

    This newer solution passes through the schematic once.

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """
    # Convert input into format which can be treated as a matrix
    f = open(file, encoding = "utf-8")
    matrix = f.read()
    matrix = matrix.split("\n")

    # Find all symbols and numbers in the matrix
    num_coor = []
    sym_coor = []
    for row, line in enumerate(matrix):
        end_col = -1
        for col, dot in enumerate(line):
            if col <= end_col:
                pass
            elif dot in SYMBOLS:
                sym_coor.append((row, col))
            elif dot.isdigit():
                start_col = col
                number, end_col = find_number(start_col, line)
                num_coor.append((row, start_col, end_col, number))


    # Find all numbers adjacent to a symbol and add them to the answer
    answer = 0
    for row, start_col, end_col, number in num_coor:
        for i, j in sym_coor:
            if (row - 1 <= i <= row + 1) and (start_col - 1 <= j <= end_col + 1):
                answer += number
                break

    return answer


print(find_part_numbers("day_3.txt"))
