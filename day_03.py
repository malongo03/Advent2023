"""
Module to solve Day 3 of the Advent of Code 2023,  which consists of the 5th and 6th stars overall.
"""
import sys

SYMBOLS = ["@", "#", "$", "%", "&", "*", "-", "+", "=", "/"]

# number_texts are stored as tuple with the following elements:
# (row_index, start_column_index, end_column_index, value)
number_text = tuple[int, int, int, int]

# symbols are stored as a tuple with following elements:
# (row_index, column_index, type)
symbol = tuple[int, int, str]


def find_number(col: int, line: str) -> tuple[int, int]:
    """
    Takes in a number's starting column in a line and returns the column it
    ends and the value of the number.

    Inputs:
        col: the column coordinate of the start of a number
        line: the line of the text that the number was found in

    """
    line_len = len(line)

    value = 0
    while col < line_len:
        cha = line[col]
        if cha.isdigit():
            value = value * 10 + int(cha)
            col += 1
        else:
            break

    return col, value


def parse_input(file: str) -> tuple[list[number_text], list[symbol]]:
    """
    Takes in an engine schematic (see Day 3 of Advent of Code 2023), and returns
    the coordinates of all the numbers and symbols.

    Input:
        file: the name/path of the input text file
    """

    with open(file, "r", encoding="utf-8") as f:
        matrix = f.read().strip().split("\n")

    numbers: list[number_text] = []
    symbols: list[symbol] = []
    for row, line in enumerate(matrix):
        end_col = -1
        for col, dot in enumerate(line):
            if col < end_col or dot == ".":
                continue
            if dot.isdigit():
                start_col = col
                end_col, number = find_number(start_col, line)
                numbers.append((row, start_col, end_col, number))
            else:
                symbols.append((row, col, dot))

    return numbers, symbols


def find_part_numbers(numbers: list[number_text], symbols: list[symbol]) -> int:
    """
    Takes in the coordinates of all the numbers and the symbols of a schematic
    and returns the sum of all the part numbers (numbers adjacent to a symbol)

    Inputs:
        numbers: the coordinates of all the numbers
        symbols: the coordinates of all the symbols
    """

    answer = 0
    for row, start_col, end_col, value in numbers:
        for i, j, _ in symbols:
            if (row - 1 <= i <= row + 1) and (start_col - 1 <= j <= end_col):
                answer += value
                break

    return answer


def find_gear_ratios(numbers: list[number_text], symbols: list[symbol]) -> int:
    """
    Takes in the coordinates of all the numbers and the symbols of a schematic,
    finds the gears (every "*" symbol with two adjacent number), calculates the
    gear ratio (the product of these numbers), and then sums the ratios of the
    entire schematic and returns.

    Inputs:
        numbers: the coordinates of all the numbers
        symbols: the coordinates of all the symbols
    """
    asterisks: dict[tuple[int, int], list[int]] =\
        {(row, col): [] for row, col, value in symbols if value == "*"}

    # Find numbers adjacent to an asterisk and add them to the adjacency
    # list of the gears
    for row, start_col, end_col, value in numbers:
        for i, j in asterisks.keys():
            if (row - 1 <= i <= row + 1) and (start_col - 1 <= j <= end_col):
                asterisks[(i, j)] = asterisks[(i, j)] + [value]
                break

    # Find which asterisks are true gears and add their gear ratios to the answer
    answer = 0
    for adj_nums in asterisks.values():
        if len(adj_nums) == 2:
            answer += adj_nums[0] * adj_nums[1]

    return answer


def main(file: str) -> None:
    parsed_numbers, parsed_symbols = parse_input(file)
    print(f"Your Star 3 answer is {find_part_numbers(parsed_numbers, parsed_symbols)}")
    print(f"Your Star 4 answer is {find_gear_ratios(parsed_numbers, parsed_symbols)}")


if __name__ == "__main__":
    main(sys.argv[1])
    sys.exit(0)
