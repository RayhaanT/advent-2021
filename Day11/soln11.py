import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day11.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

STEPS = 100

class Octopus:
    def __init__(self, energy):
        self.energy = energy
        self.neigbours = []
        self.flashed = False

    def addNeighbour(self, neighbour):
        self.neigbours.append(neighbour)

    def flash(self, chain = False):
        if self.flashed:
            return 0
        if chain:
            self.energy += 1

        if self.energy < 10:
            return 0

        self.energy = 0
        flashes = 1
        self.flashed = True
        for n in self.neigbours:
            flashes += n.flash(True)
        return flashes

def generateNeighbours(octo, octopi, x, y):
    left = x - 1 if x > 0 else None
    right = x + 1 if x < len(octopi[0]) - 1 else None
    up = y - 1 if y > 0 else None
    down = y + 1 if y < len(octopi) - 1 else None

    if left is not None:
        octo.addNeighbour(octopi[y][left])
    if right is not None:
        octo.addNeighbour(octopi[y][right])
    if up is not None:
        octo.addNeighbour(octopi[up][x])
    if down is not None:
        octo.addNeighbour(octopi[down][x])
    if left is not None and up is not None:
        octo.addNeighbour(octopi[up][left])
    if left is not None and down is not None:
        octo.addNeighbour(octopi[down][left])
    if right is not None and up is not None:
        octo.addNeighbour(octopi[up][right])
    if right is not None and down is not None:
        octo.addNeighbour(octopi[down][right])

def allFlashed(octopi):
    for row in octopi:
        for o in row:
            if not o.flashed:
                return False
    return True

def printO(octopi):
    for row in octopi:
        for o in row:
            print(o.energy, end='')
        print('')
    print('')

octopi = [[Octopus(int(c)) for c in l] for l in lines]

for y in range(0, len(octopi)):
    for x in range(0, len(octopi[y])):
        generateNeighbours(octopi[y][x], octopi, x, y)

totalFlashes = 0
counter = 0
finalCounter = 0
done = False
while not done or counter < STEPS:
    # printO(octopi)
    for row in octopi:
        for o in row:
            o.energy += 1
            o.flashed = False

    stepFlashes = 0
    for row in octopi:
        for o in row:
            stepFlashes += o.flash()

    if counter < STEPS:
        totalFlashes += stepFlashes

    counter += 1
    if not done:
        done = allFlashed(octopi)
        finalCounter = counter

# printO(octopi)

print("First: " + str(totalFlashes))
print("Second: " + str(finalCounter))
