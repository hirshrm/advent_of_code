import os

PATH = '~/advent_of_code/2025/02/rhirsh/input-small.txt'

"""
PART ONE
"""
badIDCount = 0
answer = 0
with open(os.path.expanduser(PATH), 'r') as file:
    ranges = file.readline().strip('\n').split(',')
    for ids in ranges:
        first, last = ids.split('-')
        for x in range(int(first), int(last) + 1):
            testID = str(x)
            l = len(testID)
            # if it's an odd number of digits, can't be repeated
            if l % 2 != 0:
                continue

            halfway = int(l / 2)
            left = testID[:halfway]
            right = testID[halfway:]
            if left == right:
                badIDCount += 1
                answer += int(testID)

print("PART ONE ----> ", answer)
# ANSWER: 26255179562
# GUESSED: 26255179562

"""
PART TWO
"""
badIDCount = 0
answer = 0
with open(os.path.expanduser(PATH), 'r') as file:
    ranges = file.readline().strip('\n').split(',')
    for ids in ranges:
        first, last = ids.split('-')
        for x in range(int(first), int(last) + 1):
            testID = str(x)
            l = len(testID)
            # if it's an odd number of digits, can't be repeated
            if l % 2 != 0:
                # UNLESS it is the same character
                if all(char == testID[0] for char in testID):
                    badIDCount += 1
                    answer += int(testID)
            else: 
                for n in range(1, l+1):
                    splices = [testID[i:i+n] for i in range(0, l, n)]
                    if len(splices) != 1:
                        if all(t == splices[0] for t in splices):
                            badIDCount += 1
                            answer += int(testID)

print("PART TWO ----> ", answer)
# ANSWER: 
# GUESSED: 
