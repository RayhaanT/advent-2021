import statistics
import math
import os

dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day7.txt')

with open(inputPath) as file:
    lines = file.readlines()

positions = [int(x) for x in lines[0].split(',')]
target = statistics.median(positions)

total = 0
for p in positions:
    total += abs(p - target)

print("First: " + str(total))

def sumTo(n):
    return n*(n+1)/2

mean = statistics.mean(positions)
lowMean = math.floor(mean)
highMean = math.ceil(mean)

highTotal = 0
lowTotal = 0
for p in positions:
    highTotal += sumTo(abs(p - highMean))
    lowTotal += sumTo(abs(p - lowMean))

print("Second: " + str(min(lowTotal, highTotal)))
