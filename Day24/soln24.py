import math
import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day24.txt')
rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]
instructions = [l.split(' ') for l in lines]

# This solution assumes the x and y buffers are cleared, and input
# goes to the w buffer for each digit

def varHash(v):
    if v == 'w':
        return 0
    if v == 'x':
        return 1
    if v == 'y':
        return 2
    if v == 'z':
        return 3
    return int(v)

def runCommand(op, target, source, state):
    if op == 'inp':
        state[target] = source
    elif op == 'add':
        state[target] = state[target] + source
    elif op == 'mul':
        state[target] = state[target] * source
    elif op == 'div':
        if source == 0:
            raise ValueError("Division by zero")
        state[target] = state[target] / source
        if state[target] > 0:
            state[target] = math.floor(state[target])
        else:
            state[target] = math.ceil(state[target])
    elif op == 'mod':
        if state[target] < 0 or source <= 0:
            raise ValueError("Invalid mod")
        state[target] = state[target] % source
    elif op == 'eql':
        state[target] = 1 if state[target] == source else 0

def runProgram(instructions, state):
    for i in instructions:
        try:
            if i[2] == 'x' or i[2] == 'y' or i[2] == 'z' or i[2] == 'w':
                source = state[varHash(i[2])]
            else:
                source = varHash(i[2])
            runCommand(i[0], varHash(i[1]), source, state)
        except ValueError:
            return 1
    return state[-1]

def computeZ(digits, instructionBlocks):
    block = 0
    state = [0, 0, 0, 0]
    zs = []
    for block in range(len(digits)):
        state[0] = digits[block]
        state[3] = runProgram(instructionBlocks[block], state)
        zs.append(state[3])
    return zs

MAX = [int(x) for x in '51939397989999']
MIN = [int(x) for x in '11717131211195']

currentBlock = []
instructionBlocks = []
first = True
for i in instructions:
    if i[0] == 'inp':
        if first:
            first = False
            continue
        instructionBlocks.append(currentBlock)
        currentBlock = []
    else:
        currentBlock.append(i)
instructionBlocks.append(currentBlock)

state = [0, 0, 0, 0]
zs = computeZ(MAX, instructionBlocks)
print(zs)

num = MAX
closed = [[] for i in range(14)] # (digit, z-value)
block = 13
decrement = False
while True:
    if num[block] == 0:
        if block == 0:
            raise Exception("Something very wrong")
        closed[block].append(zs[block - 1])
        num[block] = 9
        block -= 1
        decrement = True
        continue

    if block == 0:
        zs[0] = runProgram(instructionBlocks[0], [num[0], 0, 0, 0])
        num[block] -= 1
        block += 1
        decrement = False
        continue

    if block == 13:
        newZ = runProgram(instructionBlocks[13], [num[13], 0, 0, zs[12]])
        if newZ == 0:
            print(zs)
            break
        num[-1] -= 1
        continue

    if zs[block - 1] in closed[block] or zs[block - 1] > 2000000:
        num[block] = 9
        block -= 1
        decrement = True
        continue
    if decrement:
        num[block] -= 1
    else:
        decrement = True
    zs[block] = runProgram(instructionBlocks[block], [num[block], 0, 0, zs[block - 1]])
    block += 1
    decrement = False

num = [str(i) for i in num]
print("First: %s" % (''.join(num)))

num = MIN
closed = [[] for i in range(14)] # (digit, z-value)
block = 13
decrement = False
zs = computeZ(MIN, instructionBlocks)
print(zs)
while True:
    if num[block] == 10:
        if block == 0:
            raise Exception("Something very wrong")
        closed[block].append(zs[block - 1])
        num[block] = 1
        block -= 1
        decrement = True
        continue

    if block == 0:
        zs[0] = runProgram(instructionBlocks[0], [num[0], 0, 0, 0])
        num[block] += 1
        block += 1
        decrement = False
        continue

    if block == 13:
        newZ = runProgram(instructionBlocks[13], [num[13], 0, 0, zs[12]])
        if newZ == 0:
            print(zs)
            break
        num[-1] += 1
        continue

    if zs[block - 1] in closed[block] or zs[block - 1] > 2000000:
        num[block] = 1
        block -= 1
        decrement = True
        continue
    if decrement:
        num[block] += 1
    else:
        decrement = True
    zs[block] = runProgram(instructionBlocks[block], [num[block], 0, 0, zs[block - 1]])
    block += 1
    decrement = False

num = [str(i) for i in num]
print("Second: %s" % (''.join(num)))
