import os
import copy

DAY_STR = '04'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

X = 'X'
M = 'M'
A = 'A'
S = 'S'
puzzle = []

with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        puzzle.append(line.rstrip("\n"))

NUM_ROWS = len(puzzle)
NUM_COLS = len(puzzle[0])

def search_neighbors(i, j, direction, target) -> list[(int, int)]:
    viable = []
    # W
    if j > 0 and puzzle[i][j - 1] == target and (direction == 'W' or direction is None):
        viable.append((i, j - 1, 'W'))
    # E
    if j < NUM_COLS - 1 and puzzle[i][j + 1] == target and (direction == 'E' or direction is None):
        viable.append((i, j + 1, 'E'))
    # N
    if i > 0 and puzzle[i - 1][j] == target and (direction == 'N' or direction is None):
        viable.append((i - 1, j, 'N'))
    # S
    if i < NUM_ROWS - 1 and puzzle[i + 1][j] == target and (direction == 'S' or direction is None):
        viable.append((i + 1, j, 'S'))
    # NW
    if i > 0 and j > 0 and puzzle[i - 1][j - 1] == target and (direction == 'NW' or direction is None):
        viable.append((i - 1, j - 1, 'NW'))
    # NE
    if i > 0 and j < NUM_COLS - 1 and puzzle[i - 1][j + 1] == target and (direction == 'NE' or direction is None):
        viable.append((i - 1, j + 1, 'NE'))
    # SE
    if i < NUM_ROWS - 1 and j < NUM_COLS - 1 and puzzle[i + 1][j + 1] == target and (direction == 'SE' or direction is None):
        viable.append((i + 1, j + 1, 'SE'))
    # SW
    if i < NUM_ROWS - 1 and j > 0 and puzzle[i + 1][j - 1] == target and (direction == 'SW' or direction is None):
        viable.append((i + 1, j - 1, 'SW'))

    return viable


#####################
def part_one():
    total_xmas = 0
    for i, row in enumerate(puzzle):
        for j, col in enumerate(row):
            if puzzle[i][j] == X:
                valid_m = search_neighbors(i, j, None, M)
                for loc_m in valid_m:
                    temp_i, temp_j, direction = loc_m
                    valid_a = search_neighbors(temp_i, temp_j, direction, A)
                    for loc_a in valid_a:
                        temp_i, temp_j, direction = loc_a
                        valid_s = search_neighbors(temp_i, temp_j, direction, S)
                        total_xmas += len(valid_s)

    print("total XMAS ----->", total_xmas)


#####################
def opposite(letter) -> str:
    if letter == M:
        return S
    return M


def is_mas(i, j, location) -> bool:
    # location will be: Top Left (TL) or Top Right (TR)
    if puzzle[i][j] != M and puzzle[i][j] != S:
        return False

    if location == 'TL':
        # MAS/SAM must go SE
        if i < NUM_ROWS - 1 and j < NUM_COLS - 1 and puzzle[i + 1][j + 1] == A:
            temp_i = i + 1
            temp_j = j + 1
            if temp_i < NUM_ROWS - 1 and temp_j < NUM_COLS - 1 and puzzle[temp_i + 1][temp_j + 1] == opposite(puzzle[i][j]):
                return True
            
    if location == 'TR':
        # MAS/SAM must go SW
        if i < NUM_ROWS - 1 and j > 0 and puzzle[i + 1][j - 1] == A:
            temp_i = i + 1
            temp_j = j - 1
            if temp_i < NUM_ROWS - 1 and temp_j > 0 and puzzle[temp_i + 1][temp_j - 1] == opposite(puzzle[i][j]):
                return True

    return False


def part_two():
    # MAS or SAM has to start/end in all 4 corners of a sliding 3x3 window
    total_x_mas = 0
    for i in range(NUM_ROWS - 2):
        for j in range(NUM_COLS - 2):
            if is_mas(i, j, 'TL') and is_mas(i, j + 2, 'TR'):
                total_x_mas += 1

    print("total X-MAS ----->", total_x_mas)


part_one()
part_two()
