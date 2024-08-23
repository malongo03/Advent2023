"""
Module to solve the first star of Day 5 of the Advent of Code 2023, which is
the 9th star overall.
"""
import sys


def assemble_piecewise(piecewise_data):
    """
    A subfunction of the parser. This takes in the text string for one of the
    maps and translates it into array before sorting the output.

    The map consists of two ranges that are bijected with the operation that
    the nth element of the source range maps to the nth element of the
    destination range. This is represented by giving the starting element of the
    destination range, the starting element of the source range, and the length
    of the ranges.

    Inputs:
        seeds [str]:

    Returns lst[tuple(int, int, int)]
    """
    piecewise_data = piecewise_data.split("\n")[1:]
    piecewise = []

    for line in piecewise_data:
        dest_start, source_start, seed_range = [int(num) for num in line.split()]
        piecewise.append((dest_start, source_start, seed_range))

    # Sorts the piecewise functions by their source interval. This is so we
    # don't have to iterate over these functions for every seed value: since we
    # know each seed value in the heap is greater than the last, and the same
    # for the functions, we can iterate through both lists only once with some
    # checks.
    piecewise.sort(key = lambda a: a[1])

    return tuple(piecewise)


def parse_data(file):
    """
    This function parses the input text file into a usable outputs, consisting
    of a list of seed ranges and a list of mapped ranges.

    Inputs:
        file [str]: the input file name

    Returns lst[tuple(int, int)], lst[tuple(int, int, int)]
    """
    f = open(file, encoding = "utf-8")
    text = f.read()
    text = text.split("\n\n")

    seeds = text[0].split()[1:]
    seeds = [int(seed) for seed in seeds]
    # Sorts the seed values from greatest to least. See previous comment in the
    # assemble_piecewise function.
    seeds.sort(reverse = True)

    # Generates a piecewise function for each map of the input file.
    conversion_maps = tuple([assemble_piecewise(item) for item in text[1:]])

    return seeds, conversion_maps


def compute_seeds_through_map(file):
    """
    Takes in a series of seed values and an elf almanac (see Day 5 of Advent of
    Code 2023) and processes them to find the locations that these seeds should
    be planted in. It then outputs the minimum location value.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    seeds, conversion_maps = parse_data(file)

    for convert_piecewise in conversion_maps:
        seed_heap = seeds[::]
        seeds = []
        function_id = 0

        # A heap of starting seed values are created and resolved in order. As
        # explained, both the heap and the piecewise functions are in order, and
        # this allows us to go linearly up the piecewise functions once, since
        # we know any piecewise function we've gone past can't possibly have
        # an interval containing a seed value, since the next seeds are greater
        # than the ones before.
        while seed_heap:
            seed = seed_heap.pop()

            # Unpacks a conversion function and finds the end of the range
            # of the domain of the function, along with where the current
            # seed value would map to if this is the correct function.
            dest_start, source_start, func_range = convert_piecewise[function_id]
            dest_seed = (seed - source_start) + dest_start
            source_end = source_start + func_range

            if seed >= source_end:
                # Checks if the domain of the conversion function is below the
                # current seed value. If it is, we move the index to the
                # function with the next highest domain and reset the heap.
                function_id += 1
                seed_heap.append(seed)
            elif seed < source_start:
                # Checks if the current seed is not covered by a conversion
                # function. If it is, it is unaffected by the map
                # transformation.
                seeds.append(seed)
            else:
                # The correct conversion function has been found, so the
                # transformed seed value can be appended to the outpost list
                seeds.append(dest_seed)

        seeds.sort(reverse = True)

    minimum = seeds[-1]

    return minimum


print(compute_seeds_through_map(sys.argv[1]))
