import copy
import os
dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, '../inputs/Day21.txt')

class Universe:
    def __init__(self, score1, score2, pos1, pos2, oneNext):
        self.score1 = score1
        self.score2 = score2
        self.pos1 = pos1
        self.pos2 = pos2
        self.oneNext = oneNext

    def __eq__(self, other):
        return (self.score1 == other.score1 and
                self.score2 == other.score2 and
                self.pos1 == other.pos1 and
                self.pos2 == other.pos2)

    def __hash__(self):
        return self.pos1 + self.pos2 * 10 + self.score1 * 1000 + self.score2 * 100000 + int(self.oneNext) * 100
    
    def __str__(self):
        return "%d %d %d %d %d" % (self.score1, self.score2, self.pos1, self.pos2, self.oneNext)

rawLines = []
with open(inputPath) as file:
    rawLines = file.readlines()
lines = [l.strip() for l in rawLines]

def rollDeterministic(die):
    one = max((die + 1) % 101, 1)
    two = max((one + 1) % 101, 1)
    three = max((two + 1) % 101, 1)
    return (one + two + three, three)

def move(pos, steps):
    pos += steps
    if pos > 10:
        pos = pos % 10
        if pos == 0:
            pos = 10
    return pos

pos1 = int(lines[0].split(' ')[-1])
pos2 = int(lines[1].split(' ')[-1])
player1 = 0
player2 = 0

die = 0
one = True
rolls = 0
while player1 < 1000 and player2 < 1000:
    (roll, die) = rollDeterministic(die)
    if one:
        pos1 = move(pos1, roll)
        player1 += pos1
    if not one:
        pos2 = move(pos2, roll)
        player2 += pos2
    one = not one
    rolls += 3

print("First: %d" % (min(player2, player1) * rolls))

pos1 = int(lines[0].split(' ')[-1])
pos2 = int(lines[1].split(' ')[-1])

diracPossibilities = {Universe(0, 0, pos1, pos2, True): 1}
rollPossibilities = [1, 3, 6, 7, 6, 3, 1]
nullUniverse = Universe(-1, -1, -1, -1, False)
totalUniverses = 0
p1Wins = 0

while len(diracPossibilities.values()) > 0:
    current = nullUniverse
    for k in diracPossibilities.keys():
        if current == nullUniverse:
            current = k
            continue
        if max(k.score1, k.score2) < max(current.score1, current.score2):
            current = k

    universes = diracPossibilities[current]
    print(len(diracPossibilities.keys()))
    del diracPossibilities[current]
    one = current.oneNext

    for i in range(0, 7):
        newUniverses = rollPossibilities[i]
        steps = i + 3
        newUniverse = copy.deepcopy(current)

        if one:
            newUniverse.oneNext = False
            newUniverse.pos1 = move(current.pos1, steps)
            newUniverse.score1 += newUniverse.pos1
            if newUniverse.score1 >= 21:
                totalUniverses += newUniverses * universes
                p1Wins += newUniverses * universes
            else:
                if newUniverse not in diracPossibilities.keys():
                    diracPossibilities[newUniverse] = 0
                diracPossibilities[newUniverse] += newUniverses * universes

        else:
            newUniverse.oneNext = True
            newUniverse.pos2 = move(current.pos2, steps)
            newUniverse.score2 += newUniverse.pos2
            if newUniverse.score2 >= 21:
                totalUniverses += newUniverses * universes
            else:
                if newUniverse not in diracPossibilities.keys():
                    diracPossibilities[newUniverse] = 0
                diracPossibilities[newUniverse] += newUniverses * universes

print("All universes: " + str(totalUniverses))
print("Player 1 Wins: " + str(p1Wins))
print("Player 2 Wins: " + str(totalUniverses - p1Wins))
