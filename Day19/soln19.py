import os
import copy

dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, "../inputs/Day19.txt")

with open(inputPath) as file:
    lines = file.readlines()
del lines[0]

identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def matrixMul(a, b):
    return [
        [sum([a[i][k] * b[k][j] for k in range(len(b))]) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matrixPow(a, exp):
    result = copy.deepcopy(identity)
    for _ in range(0, exp):
        result = matrixMul(result, a)
    return result


def applyMatrix(mat, vec):
    return [v[0] for v in matrixMul(mat, [[v] for v in vec])]


def squareDist(a, b):
    return sum([(a[i] - b[i]) ** 2 for i in range(len(a))])


def vectorDist(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def manhattanDist(a, b):
    return sum([abs(x) for x in vectorDist(a, b)])


# Compute length of the edges of each node
def graphEdgeLengths(scanner):
    return [
        [squareDist(scanner[i], scanner[j]) for j in range(len(scanner)) if j != i]
        for i in range(len(scanner))
    ]


# Check if 2 nodes are similar comparing the length of edges
# to their neighbours. Want 11 similar neighbours to imply a
# similar graph of size 12
def matchEdges(a, edges):
    for e in range(len(edges)):
        matches = 0
        for dist in a:
            if dist in edges[e]:
                matches += 1
            if matches == 11:
                # Add 1 to avoid 0 registering as false
                return e + 1
    return False


# Find how many nodes in each graph are similar by
# looking at distance to neighbours
def commonGraphs(base, comp):
    baseEdges = graphEdgeLengths(base)
    compEdges = graphEdgeLengths(comp)
    return [
        (base[i], comp[k - 1])
        for i in range(len(base))
        if (k := matchEdges(baseEdges[i], compEdges))
    ]


# Try to find offset and rotation of comp from base if they align
def alignScanners(base, comp, rots):
    common = commonGraphs(base, comp)
    if len(common) < 12:
        return False
    for rot in rots:
        dist = vectorDist(common[0][0], applyMatrix(rot, common[0][1]))
        match = True
        for i in range(1, len(common)):
            if vectorDist(common[i][0], applyMatrix(rot, common[i][1])) != dist:
                match = False
                break
        if match:
            return [rot, dist]
    return False


# Generate all possible rotation matrices from single rotations and their inverses
xRot = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
yRot = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
zRot = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]

rotMatrices = []
rotInverses = []
for item in [
    (
        matrixMul(
            matrixMul(matrixPow(xRot, i), matrixPow(yRot, j)), matrixPow(zRot, k)
        ),
        matrixMul(
            matrixMul(matrixPow(zRot, 4 - k), matrixPow(yRot, 4 - j)),
            matrixPow(xRot, 4 - i),
        ),
    )
    for i in range(4)
    for j in range(4)
    for k in range(4)
]:
    if item not in rotMatrices:
        rotMatrices.append(item[0])
        rotInverses.append(item[1])

# Parse input
scannerBlocks = [[]]
for line in lines:
    if len(line) < 2:
        scannerBlocks.append([])
        continue
    if line[1] == "-":
        continue
    else:
        scannerBlocks[-1].append([int(coord) for coord in line.split(",")])

# Find all scanner alignments
alignments = [False for _ in range(len(scannerBlocks))]
alignments[0] = [identity, [0, 0, 0]]
lastSolve = 0
while False in alignments:
    for i in range(len(scannerBlocks)):
        if alignments[i]:
            continue
        if transform := alignScanners(
            scannerBlocks[lastSolve], scannerBlocks[i], rotMatrices
        ):
            # Transform offset/rotation to align with scanner 0 instead of lastSolve
            # Apply rotation to reference
            transform[0] = matrixMul(alignments[lastSolve][0], transform[0])
            # Apply reference rotation to offset and add to reference offset
            transform[1] = applyMatrix(alignments[lastSolve][0], transform[1])
            transform[1] = [
                alignments[lastSolve][1][i] + transform[1][i]
                for i in range(len(transform[1]))
            ]
            alignments[i] = transform
            os.system("clear")
            for align in alignments:
                print(align)
    lastSolve = (lastSolve + 1) % len(scannerBlocks)
    while not alignments[lastSolve]:
        lastSolve = (lastSolve + 1) % len(scannerBlocks)

# Compute unique beacon locations
beacons = []
for i in range(len(scannerBlocks)):
    invRot = rotInverses[rotMatrices.index(alignments[i][0])]
    offset = alignments[i][1]
    for b in scannerBlocks[i]:
        trueB = copy.deepcopy(b)
        trueB = applyMatrix(alignments[i][0], trueB)
        trueB = [trueB[j] + offset[j] for j in range(len(trueB))]
        if trueB not in beacons:
            beacons.append(trueB)

print("First: " + str(len(beacons)))

# Maximum manhattan distance
maxDist = max(
    [
        manhattanDist(alignments[i][1], alignments[j][1])
        for i in range(len(scannerBlocks))
        for j in range(len(scannerBlocks))
        if i != j
    ]
)
print("Second: " + str(maxDist))
