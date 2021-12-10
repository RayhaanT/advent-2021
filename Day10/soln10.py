import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day10.txt')

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

charPairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
closeChars = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
closeCharsIncomplete = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

class Chunk:
    def __init__(self, openChar):
        self.openChar = openChar
        self.closed = False

    def close(self, closeCandidate):
        if charPairs[self.openChar] == closeCandidate:
            self.closed = True
            return True
        return False

    def getCloser(self):
        return charPairs[self.openChar]

autocompleteScores = []
score = 0
for l in lines:
    corrupted = False
    chunks = []
    for c in l:
        if c in charPairs.keys():
            chunks.append(Chunk(c))
        else:
            success = chunks[-1].close(c)
            if success:
                chunks = chunks[:-1]
            elif not corrupted:
                score += closeChars[c]
                corrupted = True
    if not corrupted:
        lineScore = 0
        for chunk in reversed(chunks):
            lineScore *= 5
            lineScore += closeCharsIncomplete[chunk.getCloser()]
        autocompleteScores.append(lineScore)

print("First: " + str(score))

autocompleteScores.sort()
middleIndex = int((len(autocompleteScores) - 1)/2)
print("Second: " + str(autocompleteScores[middleIndex]))
