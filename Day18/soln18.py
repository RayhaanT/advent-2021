import itertools
import copy
import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day18.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

class Node:
    id_iter = itertools.count()
    def __init__(self, left, right, depth):
        self.left = left
        self.right = right
        self.depth = depth
        self.parent = None
        self.id = next(Node.id_iter)
        self.updateChildren()

    def __eq__(self, other):
        if type(other) is int:
            return False
        return self.id == other.id

    def updateChildren(self):
        if type(self.left) is not int:
            self.left.parent = self
            self.left.depth = self.depth + 1
            self.left.updateChildren()
        if type(self.right) is not int:
            self.right.parent = self
            self.right.depth = self.depth + 1
            self.right.updateChildren()

def add(left, right):
    sumNode = Node(left, right, left.depth)
    return sumNode

def magnitude(node):
    if type(node) is int:
        return node
    return 3*magnitude(node.left) + 2*magnitude(node.right)

def split(n, depth):
    low = n // 2
    return Node(low, n - low, depth + 1)

def leftmost(node):
    if type(node.left) is int:
        return node
    return leftmost(node.left)

def rightmost(node):
    if type(node.right) is int:
        return node
    return rightmost(node.right)

def contains(node, keyNode):
    if type(node) is int:
        return False
    if node == keyNode:
        return True
    return contains(node.left, keyNode) or contains(node.right, keyNode)

# Assume left and right of node are regular numbers
def explode(node, tree):
    left = node.left
    right = node.right
    current = node.parent

    leftFound = False
    rightFound = False
    # Search for left and right
    while True:
        if not contains(current.left, node) and not leftFound:
            if type(current.left) is int:
                current.left += left
            else:
                update = rightmost(current.left)
                update.right += left
            leftFound = True

        if not contains(current.right, node) and not rightFound:
            if type(current.right) is int:
                current.right += right
            else:
                update = leftmost(current.right)
                update.left += right
            rightFound = True
            
        current = current.parent
        if current is None:
            break

    current = tree
    while True:
        if current.left == node:
            current.left = 0
            return
        if current.right == node:
            current.right = 0
            return
        if contains(current.left, node):
            current = current.left
        else:
            current = current.right

def probeExplodes(node, tree):
    if type(node) is int:
        return False
    if node.depth >= 4:
        explode(node, tree)
        return True
    if not probeExplodes(node.left, tree):
        return probeExplodes(node.right, tree)
    return True

def probeSplits(node):
    if type(node) is int:
        return (node, False)
    if type(node.left) is int:
        if node.left > 9:
            node.left = split(node.left, node.depth)
            return (node, True)
    left = probeSplits(node.left)
    node.left = left[0]
    if left[1]:
        return (node, True)

    if type(node.right) is int:
        if node.right > 9:
            node.right = split(node.right, node.depth)
            return (node, True)
    right = probeSplits(node.right)
    node.right = right[0]
    if right[1]:
        return (node, True)
    return (node, False)

def reduce(node):
    while True:
        node.updateChildren()
        if probeExplodes(node, node):
            continue
        if probeSplits(node)[1]:
            continue
        break
    node.updateChildren()
    return node

def parseNumber(string, depth = 0):
    if string[0] == ',':
        string = string[1:]
    if string[0] == '[':
        (left, string) = parseNumber(string[1:], depth + 1)
        (right, string) = parseNumber(string, depth + 1)
        return (Node(left, right, depth), string[1:])
        
    if string[0].isdigit():
        if string[1] == ',':
            return (int(string[0]), string[2:])
        return (int(string[0]), string[1:])

    return (0, 0)

def printNum(node):
    betterPrintNum(node)
    print('')

def printNumInner(node):
    if type(node) is int:
        print(node, end=' ')
        return
    print('Node (%d) ' % node.depth, end='')
    printNumInner(node.left)
    printNumInner(node.right)
    print('')

def betterPrintNum(node):
    if type(node) is int:
        print(node, end='')
        return
    print('[', end='')
    betterPrintNum(node.left)
    print(',', end='')
    betterPrintNum(node.right)
    print(']', end='')

numbers = []
for l in lines:
    numbers.append(parseNumber(l)[0])

first = True
runningSum = None
for num in numbers:
    n = copy.deepcopy(num)
    if first:
        runningSum = n
        first = False
        continue
    runningSum = reduce(add(runningSum, n))
print("First: " + str(magnitude(runningSum)))

maxMagnitude = 0
for x in range(0, len(numbers)):
    for y in range(0, len(numbers)):
        if x == y:
            continue
        n1 = copy.deepcopy(numbers[x])
        n2 = copy.deepcopy(numbers[y])
        newMagnitude = magnitude(reduce(add(n1, n2)))
        maxMagnitude = max(newMagnitude, maxMagnitude)

print("Second: " + str(maxMagnitude))
