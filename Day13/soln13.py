import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day13.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

def foldHorz(paper, col):
    mirroredge = min(2 * col + 1, len(paper[0]));
    for y in range(0, len(paper)):
        for x in range(1, mirroredge - col):
            paper[y][col - x] += paper[y][col + x]

    for y in range(0, len(paper)):
        paper[y] = paper[y][0:col]
    return paper

def foldVert(paper, row):
    mirroredge = min(2 * row + 1, len(paper));
    for x in range(0, len(paper[0])):
        for y in range(1, mirroredge - row):
            paper[row - y][x] += paper[row + y][x]
    return paper[0:row]

def count(paper):
    total = 0
    for row in paper:
        for dot in row:
            if dot > 0:
                total += 1
    return total

def printPaper(paper):
    for row in paper:
        for dot in row:
            if dot > 0:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print('')

instructions, coords = [], []
firstInstructionIndex = 0
width = 0
height = 0

for i in range(0, len(lines)):
    if len(lines[i]) < 2:
        firstInstructionIndex = i + 1
        break
    coords.append(lines[i])
    arr = [int(x) for x in lines[i].split(',')]
    width = max(arr[0], width)
    height = max(arr[1], height)
width += 1
height += 1

for i in range(firstInstructionIndex, len(lines)):
    instructions.append(lines[i])

paper = [[0 for x in range(0, width)] for y in range(0, height)]
for c in coords:
    arr = [int(x) for x in c.split(',')]
    paper[arr[1]][arr[0]] = 1

first = True
for fold in instructions:
    arr = fold.split(' ')
    components = arr[2].split('=')
    if components[0] == 'x':
        paper = foldHorz(paper, int(components[1]))
        width = int(components[1])
    else:
        paper = foldVert(paper, int(components[1]))
        height = int(components[1])
    if first:
        print("First: " + str(count(paper)))
        first = False
    # printPaper(paper)

print("Second:")
printPaper(paper)
