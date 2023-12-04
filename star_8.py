"""
Module to solve the second star of Day 4 of the Advent of Code 2023, which is the
8th star overall.
"""
def count_scratch_cards(file):
    """
    Takes in list of scratch cards and their numbers (see Day 4 of Advent of
    Code 2023), and counts the extra cards won by comparing the winning
    numbers to the scratched out numbers. The extra cards are won in the
    following manner:

    The first matching number wins a copy of the next card in the sequence. The
    second matching number wins a copy of the card after that, and so on.

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
        scratch_cards[index] = [1, win_num, scratch_num]

    # Counts the copies of each card, making sure to add any winnings to the
    # pile of scratch cards.
    total_cards = 0
    for day_num, day in enumerate(scratch_cards):
        index = day_num + 1
        day_copies, win_num, scratch_num = day
        total_cards += day_copies
        for num in scratch_num:
            if num in win_num:
                scratch_cards[index][0] += day_copies
                index += 1

    return total_cards

print(count_scratch_cards("day_4.txt"))
