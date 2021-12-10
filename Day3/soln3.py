import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day3.txt')

with open(inputPath) as file:
    lines = file.readlines()

lines = [l.strip() for l in lines]

oneTallies = []
total = len(lines)

for x in range(0, len(lines[0])):
    oneTallies.append(0)

for l in lines:
    for x in range(0, len(l)):
        if l[x] == '1':
            oneTallies[x] += 1

final = []
for t in oneTallies:
    if (t*2 > total):
        final.append(1)
    else:
        final.append(0)

width = len(lines[0])
delta = 0
for f in range(0, width):
    delta += (2**(width - f - 1))*final[f]

oCand = lines.copy()
cCand = lines.copy()

for index in range(0, width):
    search = 0
    oneTally = 0
    zeroTally = 0
    for l in oCand:
        if l[index] == '1':
            oneTally+=1
        else:
            zeroTally +=1

    if oneTally >= zeroTally:
        search = 1
    else:
        search = 0

    oCandCopy = oCand.copy()
    for l in range(0, len(oCand)):
        if len(oCand) == 1:
            break
        if int(oCandCopy[l][index]) != search:
            try:
                oCand.remove(oCandCopy[l])
            except IndexError:
                continue
    if len(oCand) == 1:
        break

for index in range(0, width):
    search = 0
    oneTally = 0
    zeroTally = 0
    for l in cCand:
        if l[index] == '1':
            oneTally+=1
        else:
            zeroTally +=1

    if oneTally >= zeroTally:
        search = 0
    else:
        search = 1

    cCandCopy = cCand.copy()
    for l in range(0, len(cCand)):
        if len(cCand) == 1:
            break
        if int(cCandCopy[l][index]) != search:
            try:
                cCand.remove(cCandCopy[l])
            except IndexError:
                continue
    if len(cCand) == 1:
        break

oxygen = 0
co2 = 0
for f in range(0, width):
    oxygen += int(oCand[0][f]) * (2**(width - f - 1))
    co2 += int(cCand[0][f]) * (2**(width - f - 1))

print("First: " + str(delta * (2**width - 1 - delta)))
print("Second: " + str(oxygen * co2))
