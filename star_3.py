"""
Module to solve the first star of Day 2 of the Advent of Code 2023, which is the
3rd star overall.
"""

def find_impossible_game(file):
    """
    Takes in a list of Snow Island games (see Day 2 of Advent of Code 2023), and
    returns the sum of every game that could have been played with a bag
    consisting of 12 red cubes, 13 green cubes, and 14 blue cubes.

    Inputs:
        file(str): the name of the input file

    Returns [int]
    """

    # Process input file into useable list for algorithm
    f = open(file, encoding = "utf-8")
    games_raw = f.read()
    games_raw = games_raw.split("\n")
    good_index = 0
    games = []
    for game in games_raw:
        lst = game.split(":")
        games.append(lst[1])

    # Converts each game into the list of bag pulls
    games = [line.split(";") for line in games]

    for i, game in enumerate(games):
        impossible = False
        for bag_pull in game:
            cube_counts = bag_pull.split(",")
            for count in cube_counts:
                cube_number, cube_type = count.split()
                cube_number = int(cube_number)
                if (cube_type == "blue" and cube_number > 14) or \
                   (cube_type == "green" and cube_number > 13) or \
                   (cube_type == "red" and cube_number > 12):
                    # Check if pull is impossible under criteria
                    impossible = True
                    break
            if impossible:
                break
        if not impossible:
            good_index += i + 1

    return good_index

print(find_impossible_game("day_2.txt"))
