import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day15.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

def increment(plane):
    newPlane = deepcopy(plane)
    for y in range(0, len(plane)):
        for x in range(0, len(plane[0])):
            newPlane[y][x] = (newPlane[y][x] % 9) + 1
    return newPlane

def printPlane(plane):
    for row in plane:
        for p in row:
            print(p, end='')
        print('')
    print('')

def deepcopy(plane):
    new = []
    for row in plane:
        new.append(row.copy())
    return new

plane = [[int(x) for x in row] for row in lines]
newPlane = plane
first = []
for j in range(0, 5):
    for i in range(0, 4):
        if i == 0:
            first = deepcopy(newPlane)
        newPlane = increment(newPlane)

        for y in range(0, len(newPlane)):
            plane[y + (j * len(newPlane))].extend(newPlane[y])

    if j < 4:
        newPlane = increment(first)
        plane.extend(newPlane)

printPlane(plane)
print(len(plane))
print(len(plane[0]))

strList = [''.join([str(x) for x in row]) for row in plane]
for s in strList:
    print(s)

with open(inputPath, 'w') as f:
    for s in strList:
        f.write("%s\n" % s)
