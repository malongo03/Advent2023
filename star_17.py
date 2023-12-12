"""
Module to solve the first star of Day 9 of the Advent of Code 2023, which is the
17th star overall.
"""
def next_in_polynomial_discrete_sequence(sequence):
    """
    Takes in a sequence of integers following a polynomial curve and
    recursively takes the derivative until it finds a constant sequence. It then
    goes back down the stack, returning the last value of the sequence plus the
    next value of the derivative sequence to return the next value.

    Inputs:
        sequence [list[int]]: a list of integers assumed to be evenly spaced and
            following some polynomial function.

    Returns int
    """
    diff_seq = []
    last_val = sequence[0]
    for val in sequence[1:]:
        diff_seq.append(val - last_val)
        last_val = val

    if set(diff_seq) == set([0]):
        return last_val

    next_diff = next_in_polynomial_discrete_sequence(diff_seq)
    return last_val + next_diff


def extrapolate_oasis_list(file):
    """
    Takes in a list of OASIS values over a consistent time frame (see Day 9 of
    the Advent of Code 2023) and predicts the next value of the sequence. It
    then sums these predictions

    Input:
        file [str]: the filename of the input

    Returns int
    """
    with open(file, encoding = "utf-8") as f:
        lst_of_seq = [[int(num) for num in line] for line in f.read().split("\n")]

    answer = 0
    for seq in lst_of_seq:
        answer += next_in_polynomial_discrete_sequence(seq)

    return answer

print(extrapolate_oasis_list("day_9.txt"))
