import math
import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day15.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

height = len(lines)
width = len(lines[0])

class Point:
    def __init__(self, x, y, risk):
        self.x = x
        self.y = y
        self.risk = risk
        self.cost = -1
        self.parent = None
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def getNeighbours(p: Point, plane):
    neighbours = []
    if p.x > 0:
        neighbours.append(plane[p.y][p.x - 1])
    if p.x < width - 1:
        neighbours.append(plane[p.y][p.x + 1])
    if p.y > 0:
        neighbours.append(plane[p.y - 1][p.x])
    if p.y < height - 1:
        neighbours.append(plane[p.y + 1][p.x])
    return neighbours

def heuristic(p: Point):
    return math.sqrt((p.x - width + 1)**2 + (p.y - height + 1)**2)

def score(p: Point):
    return p.cost + heuristic(p)

plane = []
for y in range(0, height):
    plane.append([])
    for x in range(0, width):
        plane[y].append(Point(x, y, int(lines[y][x])))

current = plane[0][0]
unvisited = [p for row in plane for p in row]
openSet = [plane[0][0]]
while current != plane[-1][-1]:
    first = True
    comp = 0
    for p in openSet:
        if first:
            current = p
            first = False
            comp = score(current)
            continue
        if score(p) < comp:
            comp = score(p)
            current = p
    if current == plane[-1][-1]:
        break
    openSet.remove(current)
    unvisited.remove(current)
    
    print("Checking " + str(current.x) + " " + str(current.y) + " " + str(current.risk))
    neighbours = getNeighbours(current, plane)
    for n in neighbours:
        if n in unvisited:
            tentative = current.cost + n.risk
            if tentative < n.cost or n.cost == -1:
                n.cost = tentative
                n.parent = current
            if n not in openSet:
                openSet.append(n)

current = plane[-1][-1]
total = 0
while current.parent is not None:
    total += current.risk
    current = current.parent

print("First: " + str(total))
