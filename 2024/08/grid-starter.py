import os
import copy
import math
import itertools
import re
from enum import Enum

DAY_STR = '08'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

#################################################
########### GRID HELPER FUNCTIONS ###############
#################################################
class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


def valid_position(row: int, col: int) -> bool:
    return row >= 0 and row < NUM_ROWS and col >= 0 and col < NUM_COLS

def next_step(row: int, col: int, direction: Direction) -> tuple[int, int]:
    """
    Returns (row,col) of next step
    """
    if direction.value == Direction.NORTH.value:
        return (row - 1, col)
    if direction.value == Direction.EAST.value:
        return (row, col + 1)
    if direction.value == Direction.SOUTH.value:
        return (row + 1, col)
    if direction.value == Direction.WEST.value:
        return (row, col - 1)

def mark(s: str, idx: int, new: str) -> str:
    """
    Args: 
        - s:   row string
        - idx: index of where to replace the character
        - new: new character to place
    Returns: the row string with the index specified as the new character specified.
    Usage ex: puzzle[row] = mark(puzzle[row], col, NEW)
    """
    return s[:idx] + new + s[idx + 1:]

#################################################
################ GET PUZZLE #####################
#################################################
puzzle: list[str] = []
with open(os.path.expanduser(DEBUG_PATH), 'r') as file:
    for row, line in enumerate(file):
        line = line.rstrip("\n")
        puzzle.append(line)
        for col, symbol in enumerate(line):
            # PROBABLY WANT TO DO SOMETHING HERE
            print("hello world")

NUM_ROWS = len(puzzle)
NUM_COLS = len(puzzle[0])


#####################
def part_one():
    x = 1
    print("PART ONE: total number of <> ----->", x)


#####################
def part_two():
    x = 1
    print("PART TWO: total number of <> ----->", x)



part_one()
part_two()
