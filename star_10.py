"""
Module to solve the second star of Day 5 of the Advent of Code 2023, which is
the 10st star overall.
"""
def construct_seed_array(seeds):
    """
    A subfunction of the parser. This takes in the text string for the inital
    seeds and translates it into array of ranges, defined by a starting seed
    and the length of the range.

    Inputs:
        seeds [str]: A string of seed ranges

    Returns lst[tuple(int, int)]
    """
    seeds = seeds.split()[1:]
    seeds = [int(seed) for seed in seeds]
    seed_array = []

    while seeds:
        seed, s_range = seeds[0], seeds[1]
        seeds = seeds[2:]
        seed_array.append((seed, s_range))

    seed_array.sort(key = lambda a: a[0], reverse = True)
    return seed_array

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

    seed_array = construct_seed_array(text[0])

    conversion_functions = tuple([assemble_piecewise(item) for item in text[1:]])

    return seed_array, conversion_functions


def compute_ranges_through_map(file):
    """
    Takes in a series of seed ranges and an elf almanac (see Day 5 of Advent of
    Code 2023) and processes them to find the locations that these seeds should
    be planted in. It then outputs the minimum location value.

    Inputs:
        file [str]: the input file name

    Returns int
    """
    seed_array, conversion_functions = parse_data(file)

    for convert_func in conversion_functions:
        seed_heap = seed_array[::]
        seed_array = []
        function_index = 0

        while seed_heap:
            seed, s_range = seed_heap.pop()

            dest_start, source_start, func_range = convert_func[function_index]
            dest_seed = (seed - source_start) + dest_start
            heap_start = source_start + func_range
            array_end = seed + s_range - 1

            if seed >= heap_start:
                function_index += 1
                seed_heap.append((seed, s_range))
            elif seed < source_start:
                seed_array.append((seed, s_range))
            elif heap_start > array_end:
                seed_array.append((dest_seed, s_range))
            else:
                heap_s_range = array_end - heap_start + 1
                array_s_range = heap_start - seed
                seed_array.append((dest_seed, array_s_range))
                seed_heap.append((heap_start, heap_s_range))

        seed_array.sort(key = lambda a: a[0], reverse = True)

    minimum = seed_array[-1][0]

    return minimum

print(compute_ranges_through_map("day_5.txt"))
