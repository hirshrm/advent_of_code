import os
import copy
import re

DAY_STR = '03'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'


# Pattern: "mul(abc,xyz)"
PART_ONE_REGEX = r'mul\((\d{1,3},\d{1,3})\)'
# Pattern: string between a "do()" and "don't()"
PART_TWO_REGEX = r'(?<=do\(\)).+?(?=don\'t\(\))'


def part_one(input: str) -> int:
    """
    Finds matching substrings and multiplies the two numbers to add to a running sum.
    """
    # Finds strings that match 'mul(abc,xyz)' and returns them in the format:
    #   ['712,171', '506,85', ...]
    x: list[str] = re.findall(PART_ONE_REGEX, input)

    sum = 0
    for each in x:
        pair = each.split(',')
        sum += int(pair[0]) * int(pair[1])

    return sum


with open(os.path.expanduser(PATH), 'r') as file:
    # bug in Part 2 was reading line by line
    # enabling goes across lines
    content = file.read().replace("\n", "")

    print("PART ONE: total ----->", part_one(content))

    total = 0
    # need to add 'do()' to the beginning and 'don't()' to the end so the regex is bounded
    content = "do()" + content + "don't()"
    x: list[str] = re.findall(PART_TWO_REGEX, content)

    for each in x:
        total += part_one(each)
    
    print("PART TWO: total ----->", total)
