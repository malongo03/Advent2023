"""
Module to solve the first star of Day 4 of the Advent of Code 2023, which is the
7th star overall.
"""
def count_gambling_points(file):
    """
    Takes in list of scratch cards and their numbers (see Day 4 of Advent of
    Code 2023), and counts the points each card won by comparing the winning
    numbers to the scratched out numbers. The points are calculated as follows:

    For each card, for n matching numbers: 0 if n = 0, 2^(n-1) otherwise

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """
    # Parse the input file into a usable form
    f = open(file, encoding = "utf-8")
    scratch_cards = f.read()
    scratch_cards = scratch_cards.split(("\n"))
    scratch_cards = [line.split(":")[1] for line in scratch_cards]
    for index, line in enumerate(scratch_cards):
        line = line.split("|")

        # Optaining the winning numbers
        win_num = line[0]
        win_num = win_num.split()
        win_num = [int(num) for num in win_num]

        # Optaining the scratched numbers
        scratch_num = line[1]
        scratch_num = scratch_num.split()
        scratch_num = [int(num) for num in scratch_num]
        scratch_cards[index] = (win_num, scratch_num)

    # Counting the points of each card
    points = 0
    for win_num, scratch_num in scratch_cards:
        day_points = 0
        for num in scratch_num:
            if num in win_num:
                if not day_points:
                    day_points = 1
                else:
                    day_points = day_points * 2
        points += day_points

    return points

print(count_gambling_points("day_4.txt"))
