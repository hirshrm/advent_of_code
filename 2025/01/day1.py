import os

PATH = '~/advent_of_code/2025/01/rhirsh/input-small.txt'

"""
PART ONE
"""
current = 50
answer = 0
with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        if line[0] == '#':
            continue
        direction = line[0]
        num = int(line[1:])

        if direction == 'L':
            current = (current - num) % 100
        else:
            current = (current + num) % 100

        if current == 0:
            answer += 1

print("PART ONE ----> ", answer)
# ANSWER: 995
# GUESSED: 995

"""
PART TWO
"""
current = 50
answer = 0

with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        if line[0] == '#':
            continue
        direction = line[0]
        num = int(line[1:])

        startAtZero = False
        if current == 0:
            startAtZero = True

        if direction == 'L':
            current -= num
        else:
            current += num

        # implement mod
        if current == 0:
            answer += 1

        while current >= 100 or current < 0:
            if current >= 100:
                current -= 100
                answer += 1
            else:
                # current is negative so want to "add" to 100
                current = 100 + current
                answer += 1

        # don't want to double count if we had started at 0 and went left (0 - 5 didn't hit 0 again)
        if startAtZero and direction == 'L' and current != 0:
            answer -= 1


print("PART TWO ----> ", answer)
# ANSWER: 
# GUESSED: 6845 (high), 4670 (low), 5272 (low), 5752 (low), 5856 (from claude script), 6362 (claude)
