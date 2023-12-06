"""
Module to solve the second star of Day 5 of the Advent of Code 2023, which is
the 10st star overall.
"""
def assemble_piecewise(piecewise_data):
    """
    A subfunction of the parser. This takes in the text string for one of the
    maps and translates it into array before sorting the output.

    The map consists of two ranges that are bijected with the opertation that 
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
    seeds.sort(reverse = True)

    conversion_functions = tuple([assemble_piecewise(item) for item in text[1:]])

    return seeds, conversion_functions


def compute_seeds_through_map(file):
    """
    Takes in a series of seed values and an elf almanac (see Day 5 of Advent of
    Code 2023) and processes them to find the locations that these seeds should
    be planted in. It then outputs the minimum location value.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    seeds, conversion_functions = parse_data(file)

    for convert_func in conversion_functions:
        seed_heap = seeds[::]
        seeds = []
        function_index = 0

        while seed_heap:
            seed = seed_heap.pop()

            dest_start, source_start, func_range = convert_func[function_index]
            dest_seed = (seed - source_start) + dest_start
            source_end = source_start + func_range

            if seed >= source_end:
                function_index += 1
                seed_heap.append(seed)
            elif seed < source_start:
                seeds.append(seed)
            else:
                seeds.append(dest_seed)

        seeds.sort(reverse = True)

    minimum = seeds[-1]

    return minimum

print(compute_seeds_through_map("day_5.txt"))
