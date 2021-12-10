import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day1.txt')

with open(inputPath) as file:
    lines = file.readlines()

depth = 7
last = 0
first = True
tally = 0
index = 0

windows = []
current = []

for l in lines:
    depth = int(l)
    current.append(depth)

    if (first):
        last = depth
        first = False
        index += 1
        continue
    if depth == "done":
        break
    if depth > last:
        tally+=1
    last = depth

    if index < 2:
        index += 1
        continue
    if index > 2:
        current.pop(0)
    index += 1
    windows.append(current[0] + current[1] + current[2])

slidingTally = 0
for x in range(1, len(windows)):
    if windows[x] > windows[x-1]:
        slidingTally += 1

print("First: " + str(tally))
print("Second: " + str(slidingTally))

