"""
Module to solve the first star of Day 4 of the Advent of Code 2023, which is the
7th star overall.
"""
import sys

s_cards = list[tuple[list[int], list[int]]]

def parse_input(file: str) -> s_cards:
    """
    Takes in an input text of scratch cards and their numbers (see Day 4 of
    Advent of Code 2023), and returns an s_card formated list for easy access
    of each card and their winning and scratched off numbers.
    """

    with open(file, 'r', encoding="utf-8") as f:
        raw_cards: list[str] = f.read().strip().split("\n")
        raw_cards: list[str] = [line.split(":")[1] for line in raw_cards]

    scratch_cards: s_cards = []
    for card in raw_cards:
        raw_winning, raw_scratch = card.split("|")

        winning_numbers = [int(num) for num in raw_winning.split()]
        scratched_numbers = [int(num) for num in raw_scratch.split()]

        scratch_cards.append((winning_numbers, scratched_numbers))

    return scratch_cards


def count_card_points(scratch_cards: s_cards) -> int:
    """
    Takes in list of scratch cards and counts the points each card won by
    comparing the winning numbers to the scratched out numbers. The points are
    calculated as follows:

    For each card, for n matching numbers: 0 if n = 0, 2^(n-1) otherwise

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """

    # Counting the points of each card
    points: int = 0
    for winning_numbers, scratched_numbers in scratch_cards:
        day_points: int = 0

        winning_set: set[int] = set(winning_numbers)
        for number in scratched_numbers:
            if number in winning_set:
                day_points += 1

        if day_points:
            points += 2 ** (day_points - 1)

    return points


def count_scratch_cards(scratch_cards: s_cards) -> int:
    """
    Takes in list of scratch cards and counts the extra cards won by comparing
    the winning numbers to the scratched out numbers. The extra cards are won
    in the following manner:

    The first matching number wins a copy of the next card in the sequence. The
    second matching number wins a copy of the card after that, and so on.
    """

    # Counts the copies of each card, making sure to add any winnings to the
    # pile of scratch cards.
    total_cards: int = 0

    card_counts: list[int] = [1] * len(scratch_cards)
    for card_number, card in enumerate(scratch_cards):
        card_copies: int = card_counts[card_number]
        total_cards += card_copies

        card_index: int = card_number + 1

        winning_numbers, scratched_numbers = card

        winning_set: set[int] = set(winning_numbers)
        for number in scratched_numbers:
            if number in winning_set:
                card_counts[card_index] += card_copies
                card_index += 1

    return total_cards


def main(file: str) -> None:
    cards: s_cards = parse_input(file)
    print(f"Your Star 3 answer is {count_card_points(cards)}")
    print(f"Your Star 4 answer is {count_scratch_cards(cards)}")


if __name__ == "__main__":
    main(sys.argv[1])
    sys.exit(0)
