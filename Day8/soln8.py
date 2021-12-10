import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day8.txt')

with open(inputPath) as file:
    lines = file.readlines()

def match(a, b):
    for c in a:
        if c not in b:
            return False
    return True

def exactMatch(a, b):
    return match(a, b) and match(b, a)

def inverse(word):
    everything = 'abcdefg'
    for c in word:
        everything = everything.replace(c, "")
    return everything

def common(codes):
    everything = 'abcdefg'
    final = ''
    for l in everything:
        good = True
        for c in codes:
            if l not in c:
                good = False
                break
        if good:
            final += l
    return final

def decode(tries):
    myCodes = ['' for x in range(0, 10)]
    # Look for special
    for t in tries:
        if len(t) == 2:
            myCodes[1] = t
        if len(t) == 3:
            myCodes[7] = t
        if len(t) == 4:
            myCodes[4] = t
        if len(t) == 7:
            myCodes[8] = t

    # Filter by 1s and 4s:
    for t in tries:
        if len(t) == 6:
            if not match(myCodes[1], t):
                myCodes[6] = t
            if not match(inverse(myCodes[4]), t):
                myCodes[9] = t
        if len(t) == 5:
            if match(myCodes[1], t):
                myCodes[3] = t
            if match(inverse(myCodes[4]), t):
                myCodes[2] = t

    zeroDelim = common([myCodes[2], myCodes[3], myCodes[4], myCodes[6], myCodes[9]])

    for t in tries:
        if len(t) == 6 and match(inverse(zeroDelim), t):
            myCodes[0] = t

    for t in tries:
        if len(t) == 5 and match(inverse(myCodes[2]), t):
            myCodes[5] = t

    return myCodes

firstTotal = 0
secondTotal = 0
for l in lines:
    blocks = l.split('|')
    inputs = blocks[0].strip().split(' ')
    mapping = decode(inputs)
    outputs = blocks[1].strip().split(' ')
    displayOut = 0

    for o in outputs:
        if exactMatch(o, mapping[1]) or exactMatch(o, mapping[4]) or exactMatch(o, mapping[7]) or exactMatch(o, mapping[8]):
            firstTotal += 1
    for o in range(0, len(outputs)):
        for x in range(0, 10):
            if exactMatch(outputs[o], mapping[x]):
                displayOut += x*(10**(3 - o))

    secondTotal += displayOut

print("First: " + str(firstTotal))
print("Second: " + str(secondTotal))
