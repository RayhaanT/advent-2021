import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day16.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]
hexCode = lines[0]
totalVersions = 0

def hexToBin(h):
    return bin(int(h, 16))[2:].zfill(4)

def binToDec(b):
    return int(b, 2)

def getNextRaw(code, index, n):
    return code[index:index + n]

def getNext(code, index, n):
    return binToDec(getNextRaw(code, index, n))

def padIndex(index):
    mod = (index + 1) % 4
    if mod == 0:
        return index
    return index + 4 - mod

def parseLiteral(code):
    index = 0
    literalCode = ''
    while True:
        temp = index + 1
        literalCode += getNextRaw(code, temp, 4)
        if code[index] == '0':
            break
        index += 5

    index += 5
    return (code[index:], binToDec(literalCode))

def parseLongOp(code):
    index = 0
    subLength = getNext(code, index, 15)
    index += 15
    code = code[index:]
    originalLength = len(code)
    subPackets = []
    while originalLength - len(code) < subLength:
        (code, newSub) = parsePacket(code)
        subPackets.append(newSub)

    excess = originalLength - len(code) - subLength
    return (code[excess:], subPackets)

def parseShortOp(code):
    index = 0
    subNum = getNext(code, index, 11)
    index += 11
    code = code[index:]
    subPackets = []
    for i in range(0, subNum):
        (code, newSub) = parsePacket(code)
        subPackets.append(newSub)

    return (code, subPackets)

def operate(subPackets, typeId):
    if typeId == 0:
        return sum(subPackets)
    if typeId == 1:
        total = 1
        for s in subPackets:
            total *= s
        return total
    if typeId == 2:
        return min(subPackets)
    if typeId == 3:
        return max(subPackets)
    if typeId == 5:
        return 1 if subPackets[0] > subPackets [1] else 0
    if typeId == 6:
        return 1 if subPackets[0] < subPackets [1] else 0
    if typeId == 7:
        return 1 if subPackets[0] == subPackets [1] else 0
    raise Exception('Invalid type ID for an operator packet')

def parsePacket(code):
    global totalVersions
    index = 0
    version = getNext(code, index, 3)
    index += 3
    totalVersions += version
    typeId = getNext(code, index, 3)
    index += 3
    if typeId == 4: # literal
        return parseLiteral(code[index:])
    else:
        if code[index] == '0':
            (code, subPackets) = parseLongOp(code[index + 1:])
            return (code, operate(subPackets, typeId))
        else:
            (code, subPackets) = parseShortOp(code[index + 1:])
            return (code, operate(subPackets, typeId))

code = ''
for c in hexCode:
    code += hexToBin(c)

output = parsePacket(code)[1]
print("First: " + str(totalVersions))
print("Second: " + str(output))
