import math
import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day14.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

polymer = {}
for i in range(1, len(lines[0])):
    pattern = lines[0][i - 1] + lines[0][i]
    if pattern not in polymer.keys():
        polymer[pattern] = 0
    polymer[pattern] += 1

lines = lines[2:]

def polymerize(base, rules):
    output = base.copy()
    for pair in base.keys():
        if pair in rules.keys():
            left = pair[0] + rules[pair]
            right = rules[pair] + pair[1]
            if left not in output.keys():
                output[left] = 0
            if right not in output.keys():
                output[right] = 0
            num = base[pair]
            output[pair] -= num
            output[left] += num
            output[right] += num
    return output

def diff(polymer):
    totals = {}
    for pattern, num in polymer.items():
        if pattern[0] not in totals.keys():
            totals[pattern[0]] = 0
        if pattern[1] not in totals.keys():
            totals[pattern[1]] = 0
        totals[pattern[0]] += num
        totals[pattern[1]] += num

    ordered = sorted(totals.values())
    return math.floor(ordered[-1]/2 - math.floor(ordered[0]/2)) + 1

rules = {}

for l in lines:
    split = l.split(' ')
    rules[split[0]] = split[2]

STEPS = 10
for i in range(0, STEPS):
    polymer = polymerize(polymer, rules)

print("First: " + str(diff(polymer)))

STEPS = 30
for i in range(0, STEPS):
    polymer = polymerize(polymer, rules)

print("Second: " + str(diff(polymer)))
