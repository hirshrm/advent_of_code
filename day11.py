import os
import copy
import math
import itertools
import re
from enum import Enum
import queue
import datetime as dt

DAY_STR = '11'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

input: list[str] = []
with open(os.path.expanduser(PATH), 'r') as file:
    for row, line in enumerate(file):
        input = line.rstrip("\n").split()

input = [int(x) for x in input]


#####################
NUM_ITER = 25
def part_one_dp(total_pebbles: int) -> int:
    print("START ---> ", dt.datetime.now())
    while not Q.empty():
        num, iteration = Q.get()
        if iteration == NUM_ITER:
            continue
        if num == 0:
            # 0 turns into a 1
            Q.put((1, iteration + 1))
        elif len(str(num)) % 2 == 0:
            # even number of digits get split in half
            total_pebbles += 1
            num_str = str(num)
            mid = len(num_str) // 2

            first_half = int(num_str[:mid])
            second_half = int(num_str[mid:])
            Q.put((first_half, iteration + 1))
            Q.put((second_half, iteration + 1))
        else:
            # stone is multiplied by 2024
            Q.put((num * 2024, iteration + 1))

    print("END   ---> ", dt.datetime.now())
    return total_pebbles


shortcut = {}
def part_two_dp(num: int, iteration: int) -> int:
    # base case: if reached num of iterations, return 1 pebble
    if iteration == NUM_ITER:
        return 1
    # if we've already been here, return the result
    if (num, iteration) in shortcut:
        return shortcut[(num, iteration)]

    # otherwise, have to solve anew
    if num == 0:
        # 0 turns into a 1
        result = part_two_dp(1, iteration + 1)
    elif len(str(num)) % 2 == 0:
        # even number of digits get split in half
        num_str = str(num)
        mid = len(num_str) // 2

        first_half = int(num_str[:mid])
        second_half = int(num_str[mid:])
        result = part_two_dp(first_half, iteration + 1) + part_two_dp(second_half, iteration + 1)
    else:
        # stone is multiplied by 2024
        result = part_two_dp(num * 2024, iteration + 1)

    # save the new entry in shortcut dictionary
    shortcut[(num, iteration)] = result
    return result


#####################
NUM_ITER = 25
Q = queue.Queue()
for num in input:
    # queue: number and how many blinks it has undergone
    Q.put((num, 0))
total_pebbles = part_one_dp(len(input))
print(f"PART ONE: total pebbles after {NUM_ITER} iterations ----->", total_pebbles)

print()
print()

# reset for part two
NUM_ITER = 75
total = 0
print("START ---> ", dt.datetime.now())
for num in input:
    total += part_two_dp(num=num, iteration=0)
print("END   ---> ", dt.datetime.now())
print(f"PART TWO: total pebbles after {NUM_ITER} iterations ----->", total)