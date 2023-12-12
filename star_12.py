"""
Module to solve the second star of Day 6 of the Advent of Code 2023, which is
the 12th star overall.
"""
import math
def parse_file(file):
    """
    This function parses the input text file into a usable output, consisting
    of the total time length of the race and the record distance.

    Inputs:
        file [str]: the input file name

    Returns int, int
    """
    f = open(file, encoding = "utf-8")
    text = f.read()
    time, record = text.split("\n")
    time = int("".join(time.split()[1:]))
    record = int("".join(record.split()[1:]))

    return time, record

def find_int_roots(c, b, a = 1):
    """
    A function for the quadratic formula, but finds exclusive integer upper and
    lower bounds, for use in solving a quadratic inequality.

    Inputs:
        c [int]: the coefficient of the degree 0 term
        b [int]: the coefficient of the degree 1 term
        a [int] = 1: the coefficient of the degree 2 term, default value is 1

    Returns int, int
    """
    root_1 = math.floor((-b - math.sqrt(b ** 2 - 4 * c)) / (2 * a))
    root_2 = math.ceil((-b + math.sqrt(b ** 2 - 4 * c)) / (2 * a))

    return root_1, root_2

def find_ways_to_win(file):
    """
    Takes in a large race time and race record (see Day 6 of Advent of
    Code 2023) and processes it to find the number of ways this race could be
    won. It does this by solving a quadratic inequality.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    time, record = parse_file(file)

    lower_bound, upper_bound = find_int_roots(record, -time)
    valid_times = upper_bound - lower_bound - 1

    return valid_times

print(find_ways_to_win("day_6.txt"))
