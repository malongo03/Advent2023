"""
Module to solve the first and second star of Day 15 of the Advent of Code 2023,
which are the 29th and 30th stars overall.
"""
import sys

def hash_algorithm(line):
    """
    Calculates the HASH value of an input string.

    Input:
        line [str]: an input string.

    Return int
    """
    current_value = 0
    for char in line:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value


def initialize_lenses(filename):
    """
    Takes in a list of instructions for initializing the lenses of the lava
    production facility (see Day 15 of the Advent of Code 2023). It prints the
    sum of the HASH values of the initialization instructions, and then
    simulates the initialization sequence to find the intensity of the outputted
    light.

    Input:
        filename [str]: the filename of the input.
    """
    with open(filename, encoding = "utf-8") as f:
        sequence = f.read().split(",")

    # Part 1
    # Sums HASH of instructions
    star_1_answer = 0
    for code in sequence:
        star_1_answer += hash_algorithm(code)
    print(f"The answer to Star 29 is {star_1_answer}")

    # Part 2
    # Simulates initiation
    box_dict = {box: [] for box in range(256)}
    for code in sequence:
        index = 0
        label = ""
        while True:
            if code[index] == "=" or code[index] == "-":
                operation = code[index]
                break
            else:
                label += code[index]
            index += 1
        box = hash_algorithm(label)
        existing_labels = [p_label for p_label, _ in box_dict[box]]
        if label in existing_labels:
            replace_index = existing_labels.index(label)
            if operation == "=":
                new_lens = int(code[index + 1])
                box_dict[box][replace_index] = [label, new_lens]
            else:
                box_dict[box].pop(replace_index)
        elif operation == "=":
            new_lens = int(code[index + 1])
            box_dict[box] = box_dict[box] + [[label, new_lens]]

    # Calculates and prints light intensity
    star_2_answer = 0
    for box, lens_list in box_dict.items():
        for index, lens_w_label in enumerate(lens_list):
            _, lens_power = lens_w_label
            star_2_answer += (box + 1) * (index + 1) * lens_power
    print(f"The answer to Star 30 is {star_2_answer}")


initialize_lenses(sys.argv[1])
