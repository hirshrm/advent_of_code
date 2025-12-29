import os
import copy
import math
import itertools
import re
from enum import Enum

DAY_STR = '09'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'
DEBUG_MED_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-medium.txt'

with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        input = line.rstrip("\n")

l = len(input)
num_files = math.ceil(l / 2)


#####################
def part_one():
    final_order = []
    done = False

    front_file_id = 0
    idx = 0
    ridx = 1

    back_file_id = num_files - 1
    back_file_num = int(input[-ridx])
    while not done:
        final_order.extend([front_file_id] * int(input[idx]))
        free_space = int(input[idx + 1])
        while free_space > 0:
            final_order.append(back_file_id)
            free_space -= 1
            back_file_num -= 1
            if back_file_num == 0:
                back_file_id -= 1
                ridx += 2
                back_file_num = int(input[-ridx])
        front_file_id += 1
        idx += 2

        if front_file_id >= back_file_id:
            if back_file_num > 0:
                final_order.extend([back_file_id] * back_file_num)
            done = True

    # # DEBUG
    # print("final order: ", final_order)

    checksum = 0
    for i, num in enumerate(final_order):
        checksum += i * num
    print("PART ONE: checksum ----->", checksum)


#####################
FREE = '.'
def part_two():
    final_order = []

    # NOTE: the most amount of space it can be between two files is 9 (single digit for the space)
    # free space map: { size_of_space: [idx_start, idx_start, ...] }
    free_space_map: dict[int, list[int]] = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
    }

    # id map: [ (idx_start, id, num) ]
    id_map: list[tuple[int, int, int]] = []
    for i, num in enumerate(input):
        if i % 2 == 0:
            # it's a file
            id_map.append( ( len(final_order), int(i / 2) , int(input[i]) ) )
            final_order.extend([int(i / 2)] * int(input[i]))
        else:
            # free space
            size_of_space = int(input[i])
            free_space_map[size_of_space].append(len(final_order))
            final_order.extend([FREE] * int(input[i]))

    # # DEBUG
    # print("start order: ", "".join([str(x) for x in final_order]))

    for item in reversed(id_map):
        idx_start, id, size = item
        leftmost = -1
        key = -1
        for i, k in enumerate(free_space_map):
            start_indices = free_space_map[k]
            if k < size or not start_indices:
                # space too small, move on
                continue

            # if we get here that means we can fit!
            # but is it the most left??
            candidate = start_indices[0]
            # make sure its more left than where we are starting from
            if candidate > idx_start:
                continue

            if leftmost == -1:
                leftmost = candidate
                key = k
            else:
                leftmost = min(candidate, leftmost)
                if leftmost == candidate:
                    key = k

        if leftmost != -1:
            # there's a place for it
            # place the id here
            for x in range(size):
                # replace the old with blank
                final_order[idx_start + x] = FREE
                final_order[leftmost + x] = id

            # update our free space map
            # the file has to have a non zero size so we will always remove this entry in the map
            old_idx = free_space_map[key].pop(0)

            # now put it back where it should go
            remaining_space = key - size
            free_space_map[remaining_space].append(old_idx + size)
            free_space_map[remaining_space] = sorted(free_space_map[remaining_space])

    # # DEBUG
    # print("final order: ", "".join([str(x) for x in final_order]))
    
    checksum = 0
    for i, num in enumerate(final_order):
        if num != FREE:
            checksum += i * num
    print("PART TWO: checksum ----->", checksum)


part_one()
part_two()
