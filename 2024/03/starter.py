import os
import copy

DAY_STR = '03'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'

with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        temp = line.split()
        x = 1

print("total <> ----->", x)
