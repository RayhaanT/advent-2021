import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day2.txt')

with open(inputPath) as file:
    lines = file.readlines()

depth = 0
horizontal = 0
aim = 0

for line in lines:
    arr = line.split()
    if arr[0] == "forward":
        horizontal += int(arr[1])
        depth += aim * int(arr[1])
    if arr[0] == "up":
        aim -= int(arr[1])
    if arr[0] == "down":
        aim += int(arr[1])

print("First: " + str(aim * horizontal))
print("Second: " + str(depth * horizontal))



