"""
Module to solve the second star of Day 2 of the Advent of Code 2023, which is the
4rd star overall.
"""
def count_power_games(file):
    """
    Takes in a list of Snow Island games (see Day 2 of Advent of Code 2023),
    finds the minimum number of blue, green, and red cubes that could be in the
    bag for the game, and returns the sum of the "power" of these minimum bags.

    The power of a bag is the product of the number of blue cubes, number of
    green cubes, and number of red cubes.

    Inputs:
        file(str): the name of the input file

    Returns int
    """
    f = open(file, encoding = "utf-8")
    games_raw = f.read()
    games_raw = games_raw.split("\n")
    powers = 0
    games = []

    for game in games_raw:
        cut = game.split(":")
        games.append(cut[1])

    games_list = [line.split(";") for line in games]
    for game in games_list:
        min_bag = {"blue": 0, "green": 0, "red": 0}
        for bag_pull in game:
            ball_counts = bag_pull.split(",")
            for count in ball_counts:
                cube_number, cube_type = count.split()
                cube_number = int(cube_number)
                min_bag[cube_type] = max(min_bag[cube_type], cube_number)
        powers += min_bag["blue"] * min_bag["green"] * min_bag["red"]

    return powers

print(count_power_games("day_2.txt"))
