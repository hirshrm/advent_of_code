import os
import copy
import math
import itertools
import re
from enum import Enum
import queue
import datetime as dt
from typing import Optional

DAY_STR = '24'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

class Gates():
    def __init__(self, name, equation = None,  value = None):
        self.name: str = name
        self.equation: Optional[str] = equation
        self.value: Optional[int] = value

AND = 'AND'
OR = 'OR'
XOR = 'XOR'


input: dict[str, Gates] = {}
num_z_wires: int = 0
with open(os.path.expanduser(DEBUG_PATH), 'r') as file:
    for row, line in enumerate(file):
        if line == '\n':
            continue
        elif '->' not in line:
            # initial values
            name, val = line.rstrip("\n").split()
            name = name.rstrip(':')
            input[name] = Gates(name=name, value=int(val))
            if name[0] == 'z':
                num_z_wires += 1
        else:
            eq, res = line.rstrip("\n").split('->')
            input[res] = Gates(name=res, equation=eq)
            if res[0] == 'z':
                num_z_wires += 1

x = 1

#####################
def calc(w1, w2, op):
    wire1: bool = True if w1 == 1 else False
    wire2: bool = True if w2 == 1 else False

    if op == AND:
        return 1 if wire1 and wire2 else 0
    if op == OR:
        return 1 if wire1 or wire2 else 0
    if op == XOR:
        return 1 if ((wire1 and not wire2) or (wire2 and not wire1)) else 0


def part_one_dp(wire1: str, wire2: str, operation: str) -> int:
    # base case: if have both values, do the calculation
    if input[wire1].value and input[wire2].value:
        return calc(wire1, wire2, operation)

    
    part_one_dp()
    return calc()
    # otherwise, have to solve anew
    if num == 0:
        # 0 turns into a 1
        result = part_one_dp(1, iteration + 1)
    elif len(str(num)) % 2 == 0:
        # even number of digits get split in half
        num_str = str(num)
        mid = len(num_str) // 2

        first_half = int(num_str[:mid])
        second_half = int(num_str[mid:])
        result = part_one_dp(first_half, iteration + 1) + part_one_dp(second_half, iteration + 1)
    else:
        # stone is multiplied by 2024
        result = part_one_dp(num * 2024, iteration + 1)

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
