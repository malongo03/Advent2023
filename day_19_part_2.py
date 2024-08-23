"""
Module to solve the second star of Day 19 of the Advent of Code 2023, which is
the 38th star overall.
"""
import sys

def parse_operator(op_str):
    """
    Takes in the string of a rule for a workflow and parses it into the type of
    rule ("command" or "go to"), and then the destination in the case of a
    "go to," and the quality being compared, the comparison, and the destination
    in the case of a "compare."

    Input:
        rule_str [str]: the raw string of the workflow rule.

    Returns tuple(str) or tuple(str, str, int, str)
    """
    op_str = op_str.split(":")
    *op_str, destination = op_str
    if not op_str:
        return "go to", destination
    quality = op_str[0][0]
    comparison = op_str[0][1]
    new_bound = int(op_str[0][2:])
    return "compare", quality, comparison, new_bound, destination


def parse_input(filename):
    """
    Takes in the test for the workflows and items, discards the items, and
    splits the text for the workflows into a dictionary, where the key is the
    name of a workflow and the value is a list of parsed rules.

    Input:
        raw_workflows [str]: the raw string data for the workflows.

    Returns dict{str: lst[tuple(str)]}
    """
    with open(filename, encoding = "utf-8") as f:
        raw_workflows, _ = f.read().split("\n\n")
    workflows = {}
    raw_workflows = raw_workflows.split()
    for line in raw_workflows:
        line = line.split("{")
        workflow, op_strs = line[0], line[1][:-1].split(",")
        operations = [parse_operator(op_str) for op_str in op_strs]
        workflows[workflow] = operations
    return workflows


def graph_workflows(workflows):
    """
    Takes in a dictionary of Elf workflows (see Day 19 of the Advent of Code
    2023) and calculates how many possible items will be accepted by these
    workflows.

    Input:
        workflows [dict{str: lst[tuple(str, int)]}]

    Return int
    """

    def follow_decision_tree(directory, ranges):
        """
        Takes in a workflow directory name and a range of item values and
        returns the number of possible items from that range that will be
        accepted if passed to this workflow.

        This is a subfunction of graph_workflow so that it can borrow its
        dictionary of workflows and so that it must be imported if
        graph_workflows is imported.

        Inputs:
            directory [str]: the name of the workflow that the ranges are being
                processed by.
            ranges [dict{str: lst[int, int]}]: the ranges (inclusive) of integer
                values for each item quality that an item can have,

        Returns int
        """
        # The two base cases.
        if directory == "A":
            # If the range is accepted, we calculate the number of possible
            # items that can arrive at this leaf and return the
            possibilities = 1
            for lower_bound, upper_bound in ranges.values():
                possibilities = possibilities * (upper_bound - lower_bound + 1)
            return possibilities
        if directory == "R":
            return 0

        # Recursive case
        commands = workflows[directory]
        possibilities = 0
        for operation, *rest in commands:
            if operation == "go to":
                # Passes the range of items to the next designated workflow
                destination = rest[0]
                possibilities += follow_decision_tree(destination, ranges)
            else:
                # Performs a comparison and adjusts ranges/makes a recurse call
                # as needed.
                new_ranges = ranges.copy()
                quality, comparison, new_bound, destination = rest
                lower_bound, upper_bound = ranges[quality]
                if comparison == "<":
                    if upper_bound < new_bound:
                        # This means that the entire range of items succeeds the
                        # comparison, and so should be passed to the next
                        # workflow to calculate the possibilities.
                        possibilities += follow_decision_tree(destination, ranges)
                        break
                    elif lower_bound < new_bound:
                        # This means that part of the range will be passed onto
                        # to a new workflow, leaving part of the range behind.
                        # We split the possible items as needed and call
                        # follow_decision_tree to calculate the possiblities of
                        # accepted items from the passed on range.
                        new_ranges[quality] = [lower_bound, new_bound - 1]
                        ranges[quality] = [new_bound, upper_bound]
                        possibilities += follow_decision_tree(destination, new_ranges)
                else:
                    if lower_bound > new_bound:
                        # See the first fork from above.
                        possibilities += follow_decision_tree(destination, ranges)
                        break
                    elif upper_bound > new_bound:
                        # See the second fork from above.
                        ranges[quality] = [lower_bound, new_bound]
                        new_ranges[quality] = [new_bound + 1, upper_bound]
                        possibilities += follow_decision_tree(destination, new_ranges)
        return possibilities

    master_ranges = {"x": [1, 4000],
                     "m": [1, 4000],
                     "a": [1, 4000],
                     "s": [1, 4000]}
    answer = follow_decision_tree("in", master_ranges)
    return answer


def main(filename):
    """
    Links the output of parse_input to the input of follow_workflows, and then
    prints the outputted integer.

    Input:
        filename [str]: the filename of the input text.
    """
    workflows = parse_input(filename)
    star_2 = graph_workflows(workflows)

    print(f"The answer to Star 38 is {star_2}.")


if __name__ == "__main__":
    main(sys.argv[1])
