import os
import copy

"""
A report only counts as safe if both of the following are true:
- The levels are either all increasing or all decreasing.
- Any two adjacent levels differ by at least one and at most three.
"""

PATH = '~/advent_of_code/2024/02/rhirsh/input.txt'

def check_report(input: list[int]) -> bool:
    safe = True
    # First test if all increasing or all decreasing
    if input == sorted(input) or input == sorted(input)[::-1]:
        # Now check differ by at least one and at most three
        selected = input[0]
        i = 1
        while safe:
            if i > len(input) - 1:
                return True
            diff = abs(input[i] - selected)
            if not (diff >= 1 and diff <= 3):
                safe = False
            selected = input[i]
            i += 1
    
    return False


safe_reports = 0

with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        temp = line.split()
        report = list(map(int, temp))

        safe = check_report(report)
        safe_reports += 1 if safe else 0

        # PART TWO: check if remove one number
        while not safe:
            l = len(report)
            for i in range(l):
                foo = copy.deepcopy(report)
                foo.pop(i)
                safe = check_report(foo)
                if safe:
                    safe_reports += 1
                    break
            safe = True

print("total safe reports ----->", safe_reports)

