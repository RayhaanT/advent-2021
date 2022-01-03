import copy
import os

dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, "../inputs/Day25.txt")

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]


def moveRight(grid):
    swaps = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x - 1] == ">" and grid[y][x] == ".":
                swaps.append((y, x - 1))

    for s in swaps:
        grid[s[0]][s[1]] = "."
        grid[s[0]][s[1] + 1] = ">"

    return grid


def moveDown(grid):
    swaps = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y - 1][x] == "v" and grid[y][x] == ".":
                swaps.append((y - 1, x))

    for s in swaps:
        grid[s[0]][s[1]] = "."
        grid[s[0] + 1][s[1]] = "v"

    return grid


def step(grid):
    grid = moveRight(grid)
    grid = moveDown(grid)
    printGrid(grid)
    return grid


def printGrid(grid):
    for row in grid:
        for c in row:
            print(c, end="")
        print()
    print()


grid = [[c for c in l] for l in lines]
oldGrid = []
steps = 0
while grid != oldGrid:
    oldGrid = copy.deepcopy(grid)
    grid = step(grid)
    steps += 1

print("First: %d" % (steps))
