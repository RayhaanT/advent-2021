import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day6.txt')

with open(inputPath) as file:
    lines = file.readlines()

ages = lines[0].split(',')
ages = [int(x) for x in ages]

fish = [0 for x in range(0, 9)]

def propogate(fish, day):
    total = sum(fish)
    for i in range(0, day):
        splitters = fish[0]
        total += splitters
        oldFish = fish.copy()
        fish = [oldFish[f + 1] for f in range(0, len(oldFish) - 1)]
        fish.append(splitters)
        fish[6] += splitters
    return total

for a in ages:
    fish[a] += 1

total = len(ages)

print("First: " + str(propogate(fish, 80)))
print("Second: " + str(propogate(fish, 256)))
