"""
Module to solve Day 21 of the Advent of Code 2023, which are the 41st and
42nd stars overall.
"""
import sys
from functools import reduce

NUM_STEPS: int = 26501365
EMPTY = -1
ROCK = -2
START = -3

def count_maze(maze: list[list[int]]) -> None:
    height = len(maze)
    width = len(maze[0])

    curr_wave: list[tuple[int, int]]
    next_wave: list[tuple[int, int]]

    for row, line in enumerate(maze):
        for col, value in enumerate(line):
            if value == START:
                maze[row][col] = 0
                next_wave = [(row, col)]
                break
        else:
            continue
        break
    else:
        raise Exception

    def find_next_step(r: int, c: int) -> list[tuple[int, int]]:
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

        valid_neighbors = []

        for d_r, d_c in directions:
            n_r, n_c = r + d_r, c + d_c
            if (0 <= n_r < height) and (0 <= n_c < width) and maze[n_r][n_c] == EMPTY:
                valid_neighbors.append((n_r, n_c))

        return valid_neighbors

    # Effectively a lazy breadth first search
    while next_wave:
        curr_wave = next_wave
        next_wave = []

        for row, col in curr_wave:
            value = maze[row][col]
            unvisited_neighbors = find_next_step(row, col)

            for next_row, next_col in unvisited_neighbors:
                maze[next_row][next_col] = value + 1
                next_wave.append((next_row, next_col))


def main(file: str) -> None:
    with open(file, encoding="utf-8") as f:
        maze: list[list[int]] = [[ROCK if cha == "#" else EMPTY if cha == "." else START for cha in line]
                                 for line in f.read().strip().split("\n")]

    count_maze(maze)

    loops = (NUM_STEPS - 65) // 131

    flattened_maze: list[int] = [num for line in maze for num in line]

    part_1 = reduce(lambda x, y: x + (y % 2 == 0 and 0 <= y <= 64), flattened_maze, 0)
    print(f"Your Star 1 answer is {part_1}")

    # There are technically faster ways to these comparisons by precise
    # filtering, but I found this is fast enough and the most transparent.
    full_odd = reduce(lambda x, y: x + (y % 2 == 1 and 0 <= y), flattened_maze, 0)
    full_even = reduce(lambda x, y: x + (y % 2 == 0 and 0 <= y), flattened_maze, 0)
    corner_odd = reduce(lambda x, y: x + (y % 2 == 1 and 66 <= y), flattened_maze, 0)
    corner_even = reduce(lambda x, y: x + (y % 2 == 0 and 66 <= y), flattened_maze, 0)
    part_2 = (full_odd * (loops + 1) * (loops + 1)
              + full_even * loops * loops
              - corner_odd * (loops + 1)
              + corner_even * loops)
    print(f"Your Star 2 answer is {part_2}")


if __name__ == "__main__":
    main(sys.argv[1])
    sys.exit(0)
