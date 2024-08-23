"""
Module to solve Day 1 of the Advent of Code 2023, which consists of the 1st and
2nd stars overall.
"""
import sys

DIGIT_STRINGS: dict[str, int] = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
                                 "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def find_digit(line: str, cha_index: int) -> int | None:
    """
    Takes in a line and an index and sees whether that index is a digit or
    spelled digit. Returns none if no digit is found.

    Inputs:
        line: the string to be searched for a digit
        cha_index: the index of the character to be searched for a digit
    """
    if line[cha_index].isdigit():
        return int(line[cha_index])

    word_lengths = (3, 4, 5)
    for length in word_lengths:
        if line[cha_index: cha_index + length] in DIGIT_STRINGS:
            return DIGIT_STRINGS[line[cha_index: cha_index + length]]

    return None


def unscramble_simple(lines: list[str]) -> int:
    """
    Takes in an amended elf trebuchet calibration (see Day 1 of Advent of Code
    2023), decodes it by finding the proper calibration numbers, and sums these
    calibration numbers.

    Inputs:
        file: the name of the input file
    """
    answer: int = 0

    line: str
    line_index: int
    cha: str
    # Scan each line and place the first found digit into first_digit, then do
    # the same to the line in reverse
    for line_index, line in enumerate(lines):
        for cha in line:
            if cha.isdigit():
                first_digit: int = int(cha)
                break
        else:
            raise SyntaxError("Line contains no digits.",
                              (sys.argv[1], line_index + 1, 1, line, line_index + 1, len(line)))

        for cha in reversed(line):
            if cha.isdigit():
                last_digit: int = int(cha)
                break

        answer += first_digit * 10 + last_digit

    return answer


def unscramble_complex(lines: list[str]) -> int:
    """
    Takes in an amended elf trebuchet calibration (see Day 1 of Advent of Code
    2023), decodes it by finding the proper calibration numbers (including
    possible digits that may be written out as strings) and sums these
    calibration numbers.

    Inputs:
        file(str): the name of the input file

    Returns int
    """
    answer: int = 0

    line: str
    line_index: int
    cha_index: int
    # Scan each line and place the first found digit into first_digit, then do
    # the same to the line in reverse
    for line_index, line in enumerate(lines):
        line_length: int = len(line)

        for cha_index in range(line_length):
            first_digit: int | None = find_digit(line, cha_index)
            if first_digit is not None:
                break
        else:
            raise SyntaxError("Line contains no digits or number names.",
                              (sys.argv[1], line_index + 1, 1, line, line_index + 1, len(line)))

        for cha_index in reversed(range(line_length)):
            last_digit: int | None = find_digit(line, cha_index)
            if last_digit is not None:
                break

        answer += first_digit * 10 + last_digit

    return answer


def main(filename: str) -> None:
    with open(filename, encoding="utf-8") as f:
        lines: list[str] = f.read().strip().split("\n")
    print(f"Your Star 1 answer is {unscramble_simple(lines)}")
    print(f"Your Star 2 answer is {unscramble_complex(lines)}")


if __name__ == '__main__':
    main(sys.argv[1])
    sys.exit(0)
