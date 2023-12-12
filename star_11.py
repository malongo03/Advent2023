"""
Module to solve the first star of Day 6 of the Advent of Code 2023, which is the
11st star overall.
"""
import math
def parse_file(file):
    """
    This function parses the input text file into a usable output, consisting
    a list of tuples, the tuples consisting of the time length of a race and
    the record distance of the same race.

    Inputs:
        file [str]: the input file name

    Returns int, int
    """
    f = open(file, encoding = "utf-8")
    text = f.read()
    times, records = text.split("\n")
    times = [int(time) for time in times.split()[1:]]
    records = [int(record) for record in records.split()[1:]]

    races = list(zip(times, records))
    return races

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
    Takes in a series of race times and race records (see Day 6 of Advent of
    Code 2023) and processes them to find the number of combination of ways
    these races could be won. It does this by solving a quadratic inequality.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    races = parse_file(file)

    win_combinations = 1
    for time, record in races:
        lower_bound, upper_bound = find_int_roots(record, -time)
        valid_times = upper_bound - lower_bound - 1
        win_combinations = win_combinations * valid_times

    return win_combinations

print(find_ways_to_win("day_6.txt"))
