import os
import copy
import math

DAY_STR = '05'
PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input.txt'
DEBUG_PATH = f'~/advent_of_code/2024/{DAY_STR}/rhirsh/input-small.txt'

rules: list[tuple[int]] = []
updates: list[list[int]] = []
with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        line = line.rstrip('\n')
        if line == '':
            continue

        if '|' in line:
            temp = line.split('|')
            rules.append((int(temp[0]), int(temp[1])))
        else:
            temp = line.split(',')
            updates.append([int(x) for x in temp])


#####################
valid_updates: list[list[int]] = []
invalid_updates: list[list[int]] = []

def nums_that_must_be_before(num) -> list[int]:
    return [pair[0] for pair in rules if pair[1] == num]


def sort_updates():
    # for each update:
    #   for every number x, check that:
    #       for all rules with x as the latter number:
    #           any rule dictating a number that was supposed to be before x is either before or not present
    for update in updates:
        is_valid = True
        nums_present = set(update)
        for i, num in enumerate(update):
            if not is_valid:
                break

            for b in nums_that_must_be_before(num):
                if b in nums_present and update.index(b) > i:
                    is_valid = False
                    invalid_updates.append(update)
                    break
        
        if is_valid:
            valid_updates.append(update)


def part_one():
    middle_sum = 0
    for update in valid_updates:
        middle_sum += update[(math.floor(len(update) / 2))]
    print("PART ONE: total valid updates' middles sum ----->", middle_sum)


def part_two():
    middle_sum = 0
    for update in invalid_updates:
        mapping: list[tuple] = []
        final_order: list[int] = []

        for num in update:
            # mapping of each number to all numbers that must be before it
            # ex. 13 must be proceeded by 12, 11, and 10 --> [ (13, [12, 11, 10]) ]

            # only care about the numbers that are in the update list
            before_nums = [x for x in nums_that_must_be_before(num) if x in update]
            mapping.append((num, before_nums))

        # tautology: at least one element MUST have nothing required to be before it
        def length_of_befores(map: tuple[int, list[int]]):
            return len(map[1])

        # sort by number of elements that must be before
        mapping.sort(key=length_of_befores)
        # grab all the first elements of the mapping -- the sort put them in the correct order
        final_order = list(zip(*mapping))[0]
        middle_sum += final_order[(math.floor(len(final_order) / 2))]

    print("PART TWO: total invalid updates' middles sum ----->", middle_sum)


# prereq
sort_updates()

part_one()
part_two()