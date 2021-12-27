import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day22.txt')
rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

class Zone:
    def __init__(self, lowX, highX, lowY, highY, lowZ, highZ):
        self.xInterval = (lowX, highX)
        self.yInterval = (lowY, highY)
        self.zInterval = (lowZ, highZ)

    @staticmethod
    def makeZone(xInt, yInt, zInt):
        newZone = Zone(xInt[0], xInt[1], yInt[0], yInt[1], zInt[0], zInt[1])
        return newZone

    def volume(self):
        return ((abs(self.xInterval[1]-self.xInterval[0]) + 1)*
                (abs(self.yInterval[1]-self.yInterval[0]) + 1)*
                (abs(self.zInterval[1]-self.zInterval[0]) + 1))

    @staticmethod
    def intersection(int1, int2):
        overallMin = max(int1[0], int2[0])
        overallMax = min(int1[1], int2[1])
        if overallMax >= overallMin:
            return (overallMin, overallMax)
        return None

    def overlaps(self, other):
        if not (xAnd := Zone.intersection(self.xInterval, other.xInterval)):
            return None
        if not (yAnd := Zone.intersection(self.yInterval, other.yInterval)):
            return None
        if not (zAnd := Zone.intersection(self.zInterval, other.zInterval)):
            return None
        return Zone.makeZone(xAnd, yAnd, zAnd)

    @staticmethod
    def sliceInterval(main, cut):
        slices = [cut]
        if cut[0] > main[0]:
            slices.append((main[0], cut[0] - 1))
        if cut[1] < main[1]:
            slices.append((cut[1] + 1, main[1]))
        return slices

    def slice(self, cut):
        xRanges = Zone.sliceInterval(self.xInterval, cut.xInterval)
        yRanges = Zone.sliceInterval(self.yInterval, cut.yInterval)
        zRanges = Zone.sliceInterval(self.zInterval, cut.zInterval)

        slices = []
        for x in range(len(xRanges)):
            for y in range(len(yRanges)):
                for z in range(len(zRanges)):
                    if x == y == z == 0:
                        continue
                    slices.append(Zone.makeZone(xRanges[x], yRanges[y], zRanges[z]))
        return slices

    def __eq__(self, other):
        return (
            self.xInterval == other.xInterval and
            self.yInterval == other.yInterval and
            self.zInterval == other.zInterval
        )

def parseLine(line):
    blocks = line.split(' ')
    on = True if blocks[0] == 'on' else False

    ranges = [l[2:] for l in blocks[1].split(',')]
    xInt = [int(x) for x in ranges[0].split('..')]
    yInt = [int(x) for x in ranges[1].split('..')]
    zInt = [int(x) for x in ranges[2].split('..')]
    newZone = Zone.makeZone(xInt, yInt, zInt)
    return (newZone, on)

def countUnique(zones):
    uniques = 0
    for i in range(len(zones)):
        newZones = [zones[i]]
        for j in range(i + 1, len(zones)):
            (unused, newZones) = flippedOff(zones[j], newZones)
        for z in newZones:
            uniques += z.volume()
    return uniques

def flippedOn(newZone, zones):
    total = newZone.volume()
    doubles = []
    for z in zones:
        if (overlap := newZone.overlaps(z)):
            doubles.append(overlap)

    less = countUnique(doubles)
    return total - less

def flippedOff(newZone, zones):
    offs = []
    length = len(zones)
    deleted = 0
    for z in range(length):
        if (overlap := newZone.overlaps(zones[z - deleted])):
            offs.append(overlap)
            slices = zones[z - deleted].slice(overlap)
            del zones[z-deleted]
            deleted += 1
            zones.extend(slices)

    return (countUnique(offs), zones)

onCells = 0
zones = []
firstPrinted = False
for l in lines:
    (newZone, on) = parseLine(l)
    if not firstPrinted and (abs(newZone.xInterval[0]) > 50 or
        abs(newZone.xInterval[1]) > 50 or
        abs(newZone.yInterval[0]) > 50 or
        abs(newZone.yInterval[1]) > 50 or
        abs(newZone.zInterval[0]) > 50 or
        abs(newZone.zInterval[1]) > 50):
        print("First: %d" % (onCells))
        firstPrinted = True

    if on:
        delta = flippedOn(newZone, zones)
        onCells += delta
        zones.append(newZone)
    else:
        (delta, zones) = flippedOff(newZone, zones)
        onCells -= delta

print("Second: %d" % (onCells))
