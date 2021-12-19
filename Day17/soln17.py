import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day17.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
blocks = rawLines[0].strip().split(' ')

def sumTo(n):
    return (n * (n + 1))/2

def reverseSumTo(n):
    lowest = 0
    while sumTo(lowest) < n:
        lowest += 1
    return lowest

def step(x, y, dx, dy):
    x += dx
    y += dy
    dx = max(dx - 1, 0)
    dy -= 1
    return (x, y, dx, dy)

def validTrajectory(x, y, xVel, yVel, xInterval, yInterval):
    maxY = y
    while x <= xInterval[1] and y >= yInterval[0]:
        (x, y, xVel, yVel) = step(x, y, xVel, yVel)
        maxY = max(maxY, y)
        if xInterval[0] <= x <= xInterval[1] and yInterval[0] <= y <= yInterval[1]:
            return maxY
    return None

xInterval = []
yInterval = []
for b in blocks:
    if b[0] == 'x':
        interval = b[2:]
        interval = interval[:-1]
        xInterval = [int(n) for n in interval.split('..')]
    if b[0] == 'y':
        interval = b[2:]
        yInterval = [int(n) for n in interval.split('..')]

minX = reverseSumTo(xInterval[0])
maxX = xInterval[1] + 1
minY = yInterval[0]
maxY = abs(yInterval[0])

highest = 0
total = 0
for y in range(minY, maxY + 1):
    for x in range(minX, maxX + 1):
        newHighest = validTrajectory(0, 0, x, y, xInterval, yInterval)
        if newHighest is not None:
            total += 1
            highest = max(highest, newHighest)

print("First: " + str(highest))
print("Second: " + str(total))
