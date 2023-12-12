"""
Module to solve the second star of Day 7 of the Advent of Code 2023, which is
the 14th star overall.
"""
def parse_input(file):
    """
    Parses the input file into a list of hands with their corrosponding bids.

    Input:
        file[str]: the file name of the input

    Returns lst[tuple(str, int)]
    """
    f = open(file, encoding = "utf-8")
    text = f.read()
    hands = [tuple(line.split()) for line in text.split("\n")]
    hands = [(hand, int(bid)) for hand, bid in hands]

    return hands


def categorize_hands(hands):
    """
    Takes in the input of hands and bids and sorts them by type. These types
    are, ranked by value: high card, one pair, two pairs, three of a kind,
    full house, four of a kind, and five of a kind.

    Input:
        hands[lst[tuple(str, int)]]: a list of hands with their bids

    Returns lst[lst[tuple(str, int)]]
    """
    high_card = []
    pair1 = []
    pair2 = []
    kind3 = []
    full_house = []
    kind4 = []
    kind5 = []

    for hand, bid in hands:

        # Counts how many of each card is in a hand
        card_dict = {}
        for card in hand:
            card_dict[card] = card_dict.get(card, 0) + 1

        # Temporarily treats jokers as being extra copies of the other numerous
        # card for the purpose of calculating hand type (since jokers are wild
        # cards).
        joker_number = card_dict.get("J", 0)
        if 5 > joker_number > 0:
            del card_dict["J"]
            max_val = 0
            for card, number in card_dict.items():
                if number > max_val:
                    joker_add = card
                    max_val = number
            card_dict[joker_add] = card_dict[joker_add] + joker_number

        # Uses some math schengaians and exclusive properties of each type of
        # hand to find the type with at most three comparison checks. This is
        # messy, but actually faster than a match case statement.
        count_of_cards = card_dict.values()
        unique_cards = len(card_dict)
        if unique_cards > 3:
            if unique_cards == 5:
                high_card.append((hand, bid))
            else:
                pair1.append((hand, bid))
        elif unique_cards == 3:
            if 3 not in count_of_cards:
                pair2.append((hand, bid))
            else:
                kind3.append((hand, bid))
        else:
            if 3 in count_of_cards:
                full_house.append((hand, bid))
            elif unique_cards == 2:
                kind4.append((hand, bid))
            else:
                kind5.append((hand, bid))

    return [high_card, pair1, pair2, kind3, full_house, kind4, kind5]

CARDS = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
def sort_hands(hands):
    """
    A quick sort variant to sort hands according to their place in the index
    CARDS. This is done not by highest value card to least valued card (as it
    should be), but instead an unorthodox method of comparing the first cards,
    then the second cards, and so on.

    Input:
        hands[lst[tuple(str, int)]]

    Returns lst[tuple(str, int)]
    """
    if hands == []:
        return []

    pivot_w_bid, *rest = hands
    lower_stack = []
    upper_stack = []

    pivot, _ = pivot_w_bid
    pivot_val = [CARDS.index(card) for card in pivot]

    for hand, bid in rest:
        hand_val = [CARDS.index(card) for card in hand]
        for index, val in enumerate(hand_val):
            if pivot_val[index] > val:
                lower_stack.append((hand, bid))
                break
            elif pivot_val[index] < val:
                upper_stack.append((hand, bid))
                break

    lower_stack = sort_hands(lower_stack)
    upper_stack = sort_hands(upper_stack)

    return lower_stack + [pivot_w_bid] + upper_stack

def calculate_won_bids(file):
    """
    Takes in a series of Camel Card hands and bets (see Day 7 of Advent of
    Code 2023) and processes it to rank them by their value. It then sums the
    product of their rank (by 1-indexing, least to greatest value) and their
    bid.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    hand_groups = categorize_hands(parse_input(file))

    for index, hand_type in enumerate(hand_groups):
        hand_groups[index] = sort_hands(hand_type)

    sorted_hands = []
    for hand_type in hand_groups:
        sorted_hands = sorted_hands + hand_type

    answer = 0
    for index, hand_w_bid in enumerate(sorted_hands):
        _, bid = hand_w_bid
        answer += bid * (index + 1)

    return answer

print(calculate_won_bids("day_7.txt"))
