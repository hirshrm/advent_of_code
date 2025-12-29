import os
import copy
import math
import itertools
import re

DAY_STR = '07'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

PART_ONE_OPERATORS = ['+', '*']

CONCATENATION = '|'
PART_TWO_OPERATORS = PART_ONE_OPERATORS + [CONCATENATION]


def add_paren(eq: str) -> str:
    parts: list[str] = eq.strip().split(" ")
    parts = [int(x) if x.isdigit() else x for x in parts]

    # PART TWO: possible that it was only two numbers to begin with
    # and, with concatenation, there is now one number
    if len(parts) == 1:
        return f"{parts[0]}"

    num_count = len([x for x in parts if type(x) == int])
    sol = "(" * (num_count - 1) + str(parts[0])
    for i in range(1, len(parts), 2):
        sol += parts[i] + str(parts[i+1]) + ")"
    return sol


def handle_concat(eq_in: str) -> str:
    eq = copy.deepcopy(eq_in)
    while eq.find(CONCATENATION) != -1:
        idx = eq.find(CONCATENATION)
        sub_eq = add_paren(eq[:idx])
        left_side_solve = eval(sub_eq)
        # idx+2 because there's always a space after concat
        eq = str(left_side_solve) + eq[idx + 2:]
    return eq


#####################
def solve(nums: list[str], operators: list[str]) -> bool:
    # cross product all the ways the equation coul dhappen
    combos = list(itertools.product(nums[:-1], operators))
    # break up the combos into each number and the operator
    temp = [combos[i:i + len(operators)] for i in range(0, len(combos), len(operators))]
    # cross product the sublists
    poss_eqs = list(itertools.product(*temp))

    for x in poss_eqs:
        eq = str(x) + f" {str(nums[-1])}"
        eq = eq.replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        # eq = eq.replace(f" {CONCATENATION} ", "")  # part 2 only
        if eq.find(CONCATENATION) != -1:
            # there is a concat, handle it
            eq = handle_concat(eq)
        eq = add_paren(eq)
        if eval(eq) == val:
            return True

    return False


#####################
with open(os.path.expanduser(PATH), 'r') as file:
    p1_valid_val_sum = 0
    p2_valid_val_sum = 0
    for line in file:
        val, nums = line.rstrip('\n').split(':')
        val = int(val)
        nums: list[str] = nums.strip().split()
        if not nums:
            continue

        if len(nums) == 1:
            if val == nums[0]:
                p1_valid_val_sum += val
            continue
        # now it's the case that there's at least two numbers

        # speed up: if any one number is larger than val, can't work
        for n in nums:
            if int(n) > val:
                continue

        part_one = solve(nums, PART_ONE_OPERATORS)
        # only run part two if part one is False
        if part_one:
            # valid for both parts
            p1_valid_val_sum += val
            p2_valid_val_sum += val
        else:
            # run part two on it and see
            p2_valid_val_sum += val if solve(nums, PART_TWO_OPERATORS) else 0
        

    print("PART ONE: total sum of valid values ----->", p1_valid_val_sum)
    print("PART TWO: total sum of valid values ----->", p2_valid_val_sum)
