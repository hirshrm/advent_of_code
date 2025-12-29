import os
import copy
import math
from enum import Enum
import threading
import time
import datetime as dt

DAY_STR = '06'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

OBSTACLE = '#'
START = '^'
BEEN = 'X'
EXIT = '*'

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


def turn_right(direction: Direction) -> Direction:
    return Direction(direction.value % 4 + 1)


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
    

def valid_position(row: int, col: int) -> bool:
    return row >= 0 and row < NUM_ROWS and col >= 0 and col < NUM_COLS

def mark(s: str, index: int, new: str) -> str:
    return s[:index] + new + s[index + 1:]


#################################################
################ GET PUZZLE #####################
#################################################
puzzle: list[str] = []
starting_row = -1
starting_col = -1
obstacle_pos = []  # PART TWO
with open(os.path.expanduser(PATH), 'r') as file:
    for row, line in enumerate(file):
        puzzle.append(line.rstrip("\n"))
        if START in line:
            starting_row = row
            starting_col = line.index(START)
        for col in [i for i, ltr in enumerate(line) if ltr == OBSTACLE]:
            obstacle_pos.append((row, col))

NUM_ROWS = len(puzzle)
NUM_COLS = len(puzzle[0])

GUARD_POSITIONS = set()

def part_one():
    row = starting_row
    col = starting_col
    direction = Direction.NORTH

    # been to the start
    puzzle[row] = mark(puzzle[row], col, BEEN)
    GUARD_POSITIONS.add((row, col))

    done = False
    while not done:
        next_row, next_col = next_step(row, col, direction)
        valid_pos = valid_position(next_row, next_col)
        if not valid_pos:
            # Stepped out of the puzzle, we are done
            GUARD_POSITIONS.add((row, col))
            done = True
            # need for part two
            puzzle[row] = mark(puzzle[row], col, EXIT)
        elif puzzle[next_row][next_col] == OBSTACLE:
            direction = turn_right(direction)
        else:
            # Not an obstacle, not out of the puzzle, just a new place
            row = next_row
            col = next_col
            puzzle[row] = mark(puzzle[row], col, BEEN)
            GUARD_POSITIONS.add((row, col))
    print("PART ONE: total distinct positions ----->", len(GUARD_POSITIONS))


#####################
OBSTRUCTION = 'O'
# invalid obstacles: the guard is able to get out
INVALID_OBSTACLES = set()
threads = []
set_lock = threading.Lock()

def task(p, obstacle_pos: tuple[int, int], done_flag: threading.Event):
    row = starting_row
    col = starting_col
    direction = Direction.NORTH

    done = False
    while not done and not done_flag.is_set():
        next_row, next_col = next_step(row, col, direction)
        valid_pos = valid_position(next_row, next_col)
        if not valid_pos:
            # Stepped out of the puzzle, we are done
            with set_lock:
                INVALID_OBSTACLES.add(obstacle_pos)
            done = True
            done_flag.set()
        elif p[next_row][next_col] == OBSTACLE or p[next_row][next_col] == OBSTRUCTION:
            direction = turn_right(direction)
        else:
            # Not an obstacle, not out of the puzzle, just a new place
            row = next_row
            col = next_col
            # useful in debugging to still mark where Been but not necessary
            puzzle[row] = mark(puzzle[row], col, BEEN)

def timer(done_flag: threading.Event):
    time.sleep(2)
    if not done_flag.is_set():
        done_flag.set()

def part_two():
    print("START: ", dt.datetime.now())
    all_pos = sorted(list(GUARD_POSITIONS))
    for pos in all_pos:
        p = copy.deepcopy(puzzle)
        p[pos[0]] = mark(p[pos[0]], pos[1], OBSTRUCTION)

        # flag for if the task completes, aka if the guard gets out
        done_flag = threading.Event()
        task_thread = threading.Thread(target=task, args=(p, pos, done_flag))
        timer_thread = threading.Thread(target=timer, args=(done_flag,))

        threads.append((task_thread, timer_thread, done_flag))

        task_thread.start()
        timer_thread.start()
        
    for task_thread, timer_thread, _ in threads:
        task_thread.join()
        timer_thread.join()
    print("END  : ", dt.datetime.now())
    print("PART TWO: total positions of loop obstructions ----->", len(GUARD_POSITIONS - INVALID_OBSTACLES))

part_one()
part_two()

"""
NOTE:
small input answers:
    (6, 3)  (7, 6)  (7, 7)
    (8, 1)  (8, 3)  (9, 7)
"""