"""
Module to solve Day 2 of the Advent of Code 2023, which consists of the 3rd and 4th stars overall.
"""
import sys

subset = tuple[int, str]
pull = list[subset]
game = list[pull]


def parse_input(file: str) -> list[game]:
    """
    Takes in an input text for Day 2 of the Advent of Code 2023 and returns it
    as a list of Snow Island "game"s. Each "game" is themselves a list of
    "pull"s, and each pull is a list of "subset"s which hold a quantity and a
    cube type. This hierarchy mirrors that of the problem itself, so the
    complexity is unavoidable.

    Input:
        file: the filename or path to the input file
    """
    # Process input file into usable list for algorithm
    with open(file, encoding="utf-8") as f:
        raw_games: list[str] = f.read().strip().split("\n")

    games: list[game] = []
    for raw_game in raw_games:
        draft_game = raw_game.split(":")[1].split(";")
        new_game: game = []
        for raw_pull in draft_game:
            draft_pull = raw_pull.split(",")
            new_pull: pull = []
            for raw_subset in draft_pull:
                draft_subset = raw_subset.strip().split()
                new_subset: subset = (int(draft_subset[0]), draft_subset[1])
                new_pull.append(new_subset)
            new_game.append(new_pull)
        games.append(new_game)

    return games


def find_impossible_games(games: list[game]) -> int:
    """
    Takes in a list of Snow Island games (see Day 2 of Advent of Code 2023), and
    returns the sum of every game that could have been played with a bag
    consisting of 12 red cubes, 13 green cubes, and 14 blue cubes.

    Inputs:
        file(str): the name of the input file

    Returns int
    """

    good_count = 0

    for i, bag_game in enumerate(games):
        # If an impossible condition is found, this nested loop will abort.
        # Otherwise, we can add the game number (1-counted) to the good_count
        for bag_pull in bag_game:
            for cube_quant, cube_type in bag_pull:
                if cube_type == "blue" and cube_quant > 14:
                    break
                if cube_type == "green" and cube_quant > 13:
                    break
                if cube_type == "red" and cube_quant > 12:
                    break
            else:
                continue
            break
        else:
            good_count += i + 1

    return good_count


def count_power_games(games: list[game]) -> int:
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

    powers: int = 0
    for bag_game in games:
        min_bag: dict[str, int] = {"blue": 0, "green": 0, "red": 0}
        for bag_pull in bag_game:
            for cube_quant, cube_type in bag_pull:
                min_bag[cube_type] = max(min_bag[cube_type], cube_quant)

        powers += min_bag["blue"] * min_bag["green"] * min_bag["red"]

    return powers


def main(file: str) -> None:
    parsed_games = parse_input(file)
    print(f"Your Star 3 answer is {find_impossible_games(parsed_games)}")
    print(f"Your Star 4 answer is {count_power_games(parsed_games)}")


if __name__ == '__main__':
    main(sys.argv[1])
    sys.exit(0)
