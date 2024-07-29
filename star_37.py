"""
Module to solve the first star of Day 19 of the Advent of Code 2023, which is
the 37th star overall.
"""
def parse_rules(rule_str):
    """
    Takes in the string of a rule for a workflow and parses it into the type of
    rule ("command" or "go to"), and then the destination in the case of a
    "go to," and the quality being compared, the comparison, and the destination
    in the case of a "compare."

    Input:
        rule_str [str]: the raw string of the workflow rule.

    Returns tuple(str)
    """
    rule_str = rule_str.split(":")
    *rule_str, destination = rule_str
    if not rule_str:
        return "go to", destination
    quality, comparison = rule_str[0][0], rule_str[0][1:]
    return "compare", quality, comparison, destination


def parse_workflows(raw_workflows):
    """
    Takes in the strings for the workflows and splits it into a dictionary,
    where the key is the name of a workflow and the value is a list of parsed
    rules.

    Input:
        raw_workflows [str]: the raw string data for the workflows.

    Returns dict{str: lst[tuple(str)]}
    """
    workflows = {}
    raw_workflows = raw_workflows.split()
    for line in raw_workflows:
        line = line.split("{")
        workflow, rule_strs = line[0], line[1][:-1].split(",")
        operations = [parse_rules(rule_str) for rule_str in rule_strs]
        workflows[workflow] = operations
    return workflows


def parse_items(raw_items):
    """
    Takes in the raw data for items and their quality scores and converts them
    into a list of dictionaries, where the key is the quality name and the
    value is the score.

    Returns lst[dict{str: str}]
    """
    items = []
    raw_items = raw_items.split()
    for line in raw_items:
        line = line[1: -1].split(",")
        item = {quality.split("=")[0]: quality.split("=")[1] for quality in line}
        items.append(item)
    return items

def parse_input(filename):
    """
    Parses the raw input text file and spits out processed equivalents.

    Returns dict{str: lst[tuple(str)]}, lst[dict{str: str}]
    """
    with open(filename, encoding = "utf-8") as f:
        raw_workflows, raw_items = f.read().split("\n\n")
        workflows = parse_workflows(raw_workflows)
        items = parse_items(raw_items)
    return workflows, items


def follow_workflows(workflows, items):
    """
    Takes in a list of items for processing and a series of Elf workflows (see
    Day 19 of the Advent of Code 2023) and finds which items will be accepted
    and which will be rejected. After that, it will sums up the values for the
    qualities of all of the accepted items.

    Input:
        workflows dict{str: lst[tuple(str)]}: the workflows containing rules
            to process the items.
        items lst[dict{str: str}]: the items to be processed according to the
            workflows.

    Returns int
    """
    A = []
    for item in items:
        directory = "in"
        while True:
            if directory == "A":
                A.append(item)
                break
            if directory == "R":
                break
            commands = workflows[directory]
            for operation, *rest in commands:
                if operation == "go to":
                    directory = rest[0]
                    break
                quality, comparison, destination = rest
                # pylint: disable = eval-used
                if eval(item[quality] + comparison):
                    directory = destination
                    break
    answer = 0
    for item in A:
        for value in item.values():
            answer += int(value)
    return answer


def main(filename):
    """
    Links the output of parse_input to the input of follow_workflows, and then
    prints the outputted integer.

    Input:
        filename [str]: the filename of the input text.
    """
    workflows, items = parse_input(filename)
    star_1 = follow_workflows(workflows, items)

    print(f"The answer to Star 37 is {star_1}.")


if __name__ == "__main__":
    main("day_19.txt")
