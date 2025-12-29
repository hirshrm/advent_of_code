import os
import copy
from enum import Enum
import math
import itertools
import re

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
ANTENNA_FREQS: dict[list[tuple[int, int]]] = {}

puzzle: list[str] = []
with open(os.path.expanduser(PATH), 'r') as file:
    for row, line in enumerate(file):
        line = line.rstrip("\n")
        puzzle.append(line)
        for col, symbol in enumerate(line):
            if symbol == '.':
                continue
            if symbol in ANTENNA_FREQS.keys():
                ANTENNA_FREQS[symbol].append((row, col))
            else:
                ANTENNA_FREQS[symbol] = [(row, col)]

NUM_ROWS = len(puzzle)
NUM_COLS = len(puzzle[0])


#####################
ANTINODE = '#'

def part_one():
    uniq_antinodes = set()
    for freq, locations in ANTENNA_FREQS.items():
        p = copy.deepcopy(puzzle)
        for a in locations:
            for b in locations:
                if a == b:
                    continue

                # displacement: a -> b
                displacement = (b[0] - a[0], b[1] - a[1])
                down = ( b[0] + displacement[0], b[1] + displacement[1] )
                if valid_position(down[0], down[1]):
                    # check if we've already marked it as an antinode
                    r = down[0]
                    c = down[1]
                    if p[r][c] == freq:
                        # can't have an antinode on top of its own antenna
                        continue
                    uniq_antinodes.add((r, c))

                up = ( a[0] - displacement[0], a[1] - displacement[1] )
                if valid_position(up[0], up[1]):
                    # check if we've already marked it as an antinode
                    r = up[0]
                    c = up[1]
                    if p[r][c] == freq:
                        # can't have an antinode on top of its own antenna
                        continue
                    uniq_antinodes.add((r, c))
                
        # # DEBUG
        # for line in p:
        #     print(line)
        # print()
        # print()
        # print()
    
    print("PART ONE: total number of unique antinodes ----->", len(uniq_antinodes))


#####################
def part_two():
    uniq_antinodes = set()
    for freq, locations in ANTENNA_FREQS.items():
        # add all the nodes because they are all antinodes themselves
        for l in locations:
            uniq_antinodes.add(l)

        for a in locations:
            for b in locations:
                if a == b:
                    continue

                # displacement: a -> b
                displacement = (b[0] - a[0], b[1] - a[1])
                down = ( b[0] + displacement[0], b[1] + displacement[1] )
                while valid_position(down[0], down[1]):
                    uniq_antinodes.add(( down[0], down[1] ))
                    down = ( down[0] + displacement[0], down[1] + displacement[1] )

                up = ( a[0] - displacement[0], a[1] - displacement[1] )
                while valid_position(up[0], up[1]):
                    uniq_antinodes.add(( up[0], up[1] ))
                    up = ( up[0] - displacement[0], up[1] - displacement[1] )
        # # DEBUG
        # print(sorted(list(uniq_antinodes)))
    
    print("PART TWO: total number of unique antinodes ----->", len(uniq_antinodes))



part_one()
part_two()