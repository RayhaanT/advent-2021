import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day12.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

STEPS = 100

class Cave:
    def __init__(self, name):
        self.id = name
        self.small = name.islower()
        self.neighbours = []
        self.visited = False

    def addNeighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def __eq__(self, other):
        return self.id == other.id

caves = {'start': Cave('start'), 'end': Cave('end')}

def addCave(newId):
    if newId not in caves.keys():
        caves[newId] = Cave(newId)

def parsePath(line):
    arr = line.strip().split('-')
    addCave(arr[0])
    addCave(arr[1])
    caves[arr[0]].addNeighbour(caves[arr[1]])
    caves[arr[1]].addNeighbour(caves[arr[0]])

def probe(root):
    if root.id == 'end':
        return 1
    if root.visited:
        return 0
    if root.small:
        root.visited = True
    paths = 0
    for n in root.neighbours:
        paths += probe(n)
    root.visited = False
    return paths

def doubleProbe(root, doubling, first = False):
    if root.id == 'end':
        if doubling.visited == 2:
            return 1
        return 0
    if root.id == 'start' and not first:
        return 0
    if root.visited > 0 and not root == doubling:
        return 0
    if root.visited == 2:
        return 0
    if root.small:
        root.visited += 1

    paths = 0
    for n in root.neighbours:
        paths += doubleProbe(n, doubling)
    root.visited -= 1
    return paths

for l in lines:
    parsePath(l)

paths = probe(caves['start'])
print(paths)

for c in caves.values():
    c.visited = 0

for c in caves.values():
    if c.small and not c == caves['start'] and not c == caves['end']:
        paths += doubleProbe(caves['start'], c, True)

print(paths)
