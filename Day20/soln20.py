import copy
import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day20.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

def printImage(out):
    for row in out:
        for s in row:
            print(s, end='')
        print()
    print()

def getNeighbours(grid, x, y):
    neighbours = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j == 0:
                pass
            neighbours.append(grid[y + i][x + j])
    return neighbours

def update(image, x, y, imgMap):
    neighbours = getNeighbours(image, x, y)
    neighbours.reverse()
    key = 0
    for n in range(len(neighbours)):
        if neighbours[n] == '#':
            key += 2**n
    return imgMap[key]

CYCLES = 50

imgMap = [c for c in lines[0]]
lines = lines[2:]

height = len(lines)
width = len(lines[0])
image = [['.' for x in range(width + 2*(CYCLES + 1))] for y in range(height + 2*(CYCLES + 1))]

for y in range(height):
    for x in range(width):
        image[y + CYCLES + 1][x + CYCLES + 1] = lines[y][x]
printImage(image)
pastState = copy.deepcopy(image)

for s in range(CYCLES):
    if imgMap[0] == '#':
        new = '#' if image[0][0] == '.' else '.'
        for y in range(len(image)):
            for x in range(len(image[0])):
                image[y][x] = new
    for y in range(height + 2*s + 2):
        for x in range(width + 2*s + 2):
            offset = CYCLES - s
            sy = y + offset
            sx = x + offset
            image[sy][sx] = update(pastState, sx, sy, imgMap)
    pastState = copy.deepcopy(image)
    printImage(image)

total = 0
for row in image:
    for s in row:
        if s == '#':
            total += 1
print("First: %d" % (total))
