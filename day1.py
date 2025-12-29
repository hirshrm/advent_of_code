import os

left: list[int] = []
right: list[int] = []

PATH = '~/advent_of_code/2024/01/rhirsh/input.txt'

with open(os.path.expanduser(PATH), 'r') as file:
    for line in file:
        temp = line.split()
        left.append(int(temp[0]))
        right.append(int(temp[1]))

left = sorted(left)
right = sorted(right)

l = len(left)
if l != len(right):
    exit(1)

"""
PART ONE
"""
total_distance = 0
for i in range(l):
    total_distance += abs(left[i] - right[i])

print("total distance between the lists ----->", total_distance)

"""
PART TWO
"""
total_similarity = 0
for n in left:
    total_similarity += n * right.count(n)

print("total similarity score between the lists ----->", total_similarity)
