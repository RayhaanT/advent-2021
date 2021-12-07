import statistics
import math

inFile = open('../inputs/Day7.txt')
lines = inFile.readlines()

positions = [int(x) for x in lines[0].split(',')]
target = statistics.median(positions)

total = 0
for p in positions:
    total += abs(p - target)

print("First: " + str(total))

def sumTo(n):
    return n*(n-1)/2

mean = statistics.mean(positions)
lowMean = math.floor(mean)
highMean = math.ceil(mean)

highTotal = 0
lowTotal = 0
for p in positions:
    highTotal += sumTo(abs(p - highMean) + 1)
    lowTotal += sumTo(abs(p - lowMean) + 1)

print("Second: " + str(min(lowTotal, highTotal)))
