import math
from fractions import Fraction

inFile = open('../inputs/Day5.txt')
lines = inFile.readlines()

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VentLine:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        length = math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)

        multX = -1 if end.x - start.x < 0 else 1
        multY = -1 if end.y - start.y < 0 else 1

        if math.ceil(length) == 0:
            self.slope = Coord(0, 0)
            return
        if end.y - start.y == 0:
            self.slope = Coord(multX, 0)
            return

        realSlope = Fraction(end.x - start.x, end.y - start.y)
        self.slope = Coord(abs(realSlope.numerator) * multX, abs(realSlope.denominator) * multY)

def parseLine(l):
    arr = l.split()
    try:
        first = arr[0].split(',')
        second = arr[2].split(',')
    except IndexError:
        print(arr)
    return VentLine(
        Coord(int(first[0]), int(first[1])),
        Coord(int(second[0]), int(second[1])))

floorMap = [[0]]
width = 0
height = 0

def printMap(m):
    for r in m:
        for n in r:
            print(n, end = '')
        print('')
    print('-----------------')

for l in lines:
    height = len(floorMap)
    width = len(floorMap[0])

    vent = parseLine(l)
    
    # For the answer for the first part, uncomment this
    # if vent.slope.x != 0 and vent.slope.y != 0:
    #     continue

    sizeCheckX = max(vent.start.x, vent.end.x) + 1
    sizeCheckY = max(vent.start.y, vent.end.y) + 1
    if width < sizeCheckX:
        for r in range(0, len(floorMap)):
            for x in range(0, sizeCheckX - width):
                floorMap[r].append(0)
        width = len(floorMap[0])
    if height < sizeCheckY:
        for x in range(0, sizeCheckY - height):
            newList = []
            for i in range(0, width):
                newList.append(0)
            floorMap.append(newList) 
        height = len(floorMap)

    update = vent.start
    while True:
        floorMap[update.y][update.x] += 1
        if update.x == vent.end.x and update.y == vent.end.y:
            break
        update = Coord(update.x + vent.slope.x, update.y + vent.slope.y)

total = 0
for r in floorMap:
    for n in r:
        if n > 1:
            total +=1 

# print("First: " + str(total))
print("Second: " + str(total))
