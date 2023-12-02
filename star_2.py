"""
Module to solve the second star of Day 1 of the Advent of Code 2023, which is the
1st star overall.
"""


DIGIT_STRINGS = {"one": 1, "two": 2, "three": 3, "four": 4,
                 "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def find_str_digits(letter_str):
    """
    Takes in a string and searches for a spelled digit in the last three to five
    characters

    Inputs:
        str(str): a string of letters.

    Returns [int] if digit is found, None otherwise
    """
    length = min([len(letter_str), 5])
    for i in range(3, length + 1):
        check = DIGIT_STRINGS.get(letter_str[-i:], None)
        if check is not None:
            return check

    return None

def unscamble_calibration(file):
    """
    Takes in an amended elf trebuchet calibration (see Day 1 of Advent of Code
    2023), unamends it by finding the proper calibration numbers, including
    possible digits that may be written out as strings, and sums these
    calibration numbers.

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """
    f = open(file, encoding = "utf-8")
    text = f.read()
    text = text.split()

    answer = 0

    for line in text:
        first_digit = None
        last_digit = None
        last_chas = ""
        for cha in line:
            last_chas += cha
            if cha.isdigit():
                # Numeric digit found
                last_digit = int(cha)
                if first_digit is None:
                    first_digit = int(cha)
                last_chas = ""
            elif len(last_chas) >= 3:
                # Spelt digit check
                check = find_str_digits(last_chas)
                if check is not None:
                    last_digit = check
                    if first_digit is None:
                        first_digit = check
        assert first_digit is not None and last_digit is not None
        answer += first_digit * 10 + last_digit

    return answer

print(unscamble_calibration("day_1.txt"))
