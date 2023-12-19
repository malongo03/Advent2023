"""
Module to solve the first star of Day 13 of the Advent of Code 2023, which is
the 25th star overall.
"""
def search_reflection(array, length):
    """
    Searches a 2D array of characters to find a line of reflection across the
    rows or columns (depending on the array type) of the array.

    Inputs:
        array [lst[str]]: a list of columns/rows of an 2D array of characters.
        length [int]: the number of rows/columns in the array (for row array and
            column arrays respectively).

    Returns int
    """
    next_column = array[0]
    found_reflection = False
    for index in range(1, len(array)):
        curr_column = next_column[:]
        next_column = array[index]
        if curr_column == next_column and check_reflect(array, length, index):
            found_reflection = True
            break
    if not found_reflection:
        return False, index
    return True, index

def check_reflect(array, length, reflect_index):
    """
    Checks whether a given index creates a valid reflection accross the rows
    or columns (depending on the array type) of an array.

    Inputs:
        array [lst[str]]: a list of columns/rows of an 2D array of characters.
        length [int]: the number of rows/columns in the array (for row array and
            column arrays respectively).
        reflect_index [int]: the index of reflection to check.

    Return bool
    """
    index = 2
    not_reflection = False
    while (0 <= reflect_index - index) and (reflect_index + index - 1 < length):
        if array[reflect_index - index] != array[reflect_index + index - 1]:
            not_reflection = True
            break
        index += 1
    if not_reflection:
        return False
    return True

def volcano_reflections(filename):
    """
    Takes in arrays of lava rock fields (see Day 13 of the Advent of Code 2023)
    and finds the direction and index of the reflection. Then it sums up the
    number of columns to the left of each vertical line of reflection with 100
    multiplied by the number of rows above each horizontal line of reflection.

    Input:
        filename [str]: the filename of the input file.

    Returns int
    """
    # Creates easy to iterate through representations of each lava rock field as
    # rows and columns. The list comprehensions are a mouth-full, but they do as
    # expected.
    with open(filename, encoding = "utf-8") as f:
        raw_arrays = f.read().split("\n\n")
    row_arrays = [[line for line in array.split("\n")] for array in raw_arrays]
    col_arrays = [  ["".join([line[i] for line in array.split("\n")])
                     for i in range(len(array.split("\n")[0]))]
                  for array in raw_arrays]
    arrays = ((row_arrays[i], col_arrays[i]) for i in range(len(raw_arrays)))

    answer = 0
    for row_array, col_array in arrays:
        is_row_reflection, reflect_index = search_reflection(row_array, len(row_array))
        if is_row_reflection:
            answer += 100 * reflect_index
        else:
            _, reflect_index = search_reflection(col_array, len(col_array))
            answer += reflect_index

    return answer

print(volcano_reflections("day_13.txt"))
