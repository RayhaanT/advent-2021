inFile = open('../inputs/Day9.txt')
lines = inFile.readlines()

grid = []
width = len(lines[0]) - 1
height = len(lines)

class Point:
    def __init__(self, height, x, y, basin = 0):
        self.height = height
        self.basin = basin
        self.x = x
        self.y = y
        self.drainage = None

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

for l in range(0, height):
    line = lines[l].strip()
    grid.append([])
    for c in range(0, width):
        grid[l].append(Point(int(line[c]), c, l))

def getAdjacents(grid, point):
    x = point.x
    y = point.y
    adjacents = []
    if x > 0:
        adjacents.append(grid[y][x-1])
    if x < width - 1:
        adjacents.append(grid[y][x+1])
    if y > 0:
        adjacents.append(grid[y-1][x])
    if y < height - 1:
        adjacents.append(grid[y+1][x])
    return adjacents

def isLocalMin(grid, point):
    adjacents = getAdjacents(grid, point)
    for a in adjacents:
        if(point.height >= a.height):
            return False
    return True

def probeBasin(grid, point, seen = []):
    if (isLocalMin(grid, point)):
        return point
    if p.drainage is not None:
        return p.drainage
    if p.height == 9:
        return None
    adjacents = getAdjacents(grid, point)
    endpoints = []
    seen.append(point)
    for a in adjacents:
        if(a.height < point.height):
            endpoints.append(probeBasin(grid, a, seen))
        if(a.height == point.height and a not in seen):
            endpoints.append(probeBasin(grid, a, seen))

    if len(endpoints) == 0:
        raise ValueError('Oops')

    x = endpoints[0].x
    y = endpoints[0].y
    for e in endpoints:
        if e.x != x or e.y != y:
            return None
    return endpoints[0]

total = 0

for row in grid:
    for p in row:
        probe = probeBasin(grid, p)
        if probe is not None:
            p.drainage = p
            probe.basin += 1
            
basins = []
for row in grid:
    for p in row:
        if isLocalMin(grid, p):
            total+=p.height + 1
            basins.append(p.basin)

basins.sort(reverse=True)

print("First: " + str(total))
print("Second: " + str(basins[0] * basins[1] * basins[2]))
