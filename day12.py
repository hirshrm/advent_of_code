import os
import copy
import math
import itertools
import re
from enum import Enum
import queue

DAY_STR = '12'
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
area: set[str, int] = {}
with open(os.path.expanduser(DEBUG_PATH), 'r') as file:
    for row, line in enumerate(file):
        line = line.rstrip("\n")
        puzzle.append(line)
        
        for _, char in enumerate(line):
            if char in area:
                area[char] += 1
            else:
                area[char] = 1

NUM_ROWS = len(puzzle)
NUM_COLS = len(puzzle[0])


#####################
Q = queue.Queue()
def dp(unique_ends: set[tuple[int, int]]) -> tuple[set, int]:
    rating = 0
    while not Q.empty():
        row, col = Q.get()
        if not valid_position(row, col):
            continue
        if puzzle[row][col] == TARGET:
            unique_ends.add((row, col))
            rating += 1
            continue

        for dir in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            next_row, next_col = next_step(row, col, dir)
            if valid_position(next_row, next_col) and int(puzzle[next_row][next_col]) == int(puzzle[row][col]) + 1:
                Q.put((next_row, next_col))

    return unique_ends, rating


def solve() -> tuple[set, dict]:
    total_score = 0
    total_rating = 0
    for head in trailheads:
        unique_ends = set()
        Q.put((head[0], head[1]))
        unique_ends, rating = dp(unique_ends)
        
        total_score += len(unique_ends)
        total_rating += rating

    print("PART ONE: total trailhead score ----->", total_score)
    print("PART TWO: total trailhead rating ----->", total_rating)


solve()