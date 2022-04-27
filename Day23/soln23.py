import os
import copy
from queue import PriorityQueue

dirname = os.path.dirname(__file__)
inputPath = os.path.join(dirname, "../inputs/Day23.txt")
rawLines = []
with open(inputPath) as file:
    lines = file.readlines()


class BurrowState:
    def __init__(self, rooms, hallway, cost, parent=None):
        self.rooms = rooms
        self.hallway = hallway
        self.cost = cost
        self.parent = parent

    def __eq__(self, other):
        return self.rooms == other.rooms and self.hallway == other.hallway

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        hallwayHash = 0
        for h in range(len(self.hallway)):
            if hallway[h] is None:
                continue
            hallwayHash += roomHash(hallway[h]) * (10 ** h)

        roomsHash = 0
        inRooms = 0
        for r in self.rooms:
            for a in r:
                roomsHash += roomHash(a) * (10 ** inRooms)
                inRooms += 1

        return int(str(roomsHash) + str(hallwayHash))


def roomHash(amphi):
    if amphi[0] == "A":
        return 0
    if amphi[0] == "B":
        return 1
    return 2 if amphi[0] == "C" else 3


def canHome(rooms, hallway, target, inRoom=False):
    h = roomHash(target)
    # Check if the room is ready
    for a in rooms[h]:
        if roomHash(a) != h:
            return False

    startIndex = 0
    if inRoom:
        for r in range(len(rooms)):
            if len(rooms[r]) == 0:
                continue
            if rooms[r][0] == target:
                startIndex = r * 2 + 2
    else:
        for i in range(len(hallway)):
            if hallway[i] == target:
                startIndex = i

    # Check if path is clear
    hallwayTarget = h * 2 + 2
    return pathClear(hallway, startIndex, hallwayTarget)


def configExists(rooms, hallways, closed):
    for config in closed:
        if config[0] == rooms and config[1] == hallways:
            return True
    return False


def stepCost(steps, amphi):
    return steps * (10 ** roomHash(amphi))


def roomSatisfied(room, index):
    for a in room:
        if roomHash(a) != index:
            return False
    return True


def pathClear(hallway, start, target):
    if hallway[target] is not None:
        return False
    delta = (target - start) // abs(target - start)
    for j in range(start + delta, target, delta):
        if hallway[j] is not None:
            return False
    return True


def move(rooms, hallway, closed, depth):
    # Check if any can finish
    for a in hallway:
        if a is not None and canHome(rooms, hallway, a):
            steps = abs(hallway.index(a) - (roomHash(a) * 2 + 2))
            steps += depth - len(rooms[roomHash(a)])
            newRooms = copy.deepcopy(rooms)
            newHallway = copy.deepcopy(hallway)
            newRooms[roomHash(a)].append(a)
            for h in range(len(newHallway)):
                if newHallway[h] == a:
                    newHallway[h] = None
                    break
            return [BurrowState(newRooms, newHallway, stepCost(steps, a))]

    # Check if any can finish directly
    for r in range(len(rooms)):
        if roomSatisfied(rooms[r], r):
            continue
        if canHome(rooms, hallway, rooms[r][0], True):
            steps = abs(r * 2 + 2 - (roomHash(rooms[r][0]) * 2 + 2))
            steps += depth - len(rooms[roomHash(rooms[r][0])])
            steps += 1 + depth - len(rooms[r])
            # steps += 1 if len(rooms[roomHash(rooms[r][0])]) == 1 else 2
            # steps += 2 if len(rooms[r]) == 1 else 1
            newRooms = copy.deepcopy(rooms)
            newHallway = copy.deepcopy(hallway)
            newRooms[roomHash(rooms[r][0])].append(rooms[r][0])
            newRooms[r].remove(rooms[r][0])
            return [BurrowState(newRooms, newHallway, stepCost(steps, rooms[r][0]))]

    moves = []

    for i in range(4):
        if roomSatisfied(rooms[i], i):
            continue
        newRooms = copy.deepcopy(rooms)
        newRooms[i].remove(rooms[i][0])
        for j in range(11):
            if j == 2 or j == 4 or j == 6 or j == 8:
                continue
            if hallway[j] is not None:
                continue
            if not pathClear(hallway, i * 2 + 2, j):
                continue
            hallway[j] = rooms[i][0]
            steps = 2 if len(rooms[i]) == 1 else 1
            steps = 1 + depth - len(rooms[i])
            steps += abs((i * 2 + 2) - j)
            newState = BurrowState(
                newRooms, copy.deepcopy(hallway), stepCost(steps, rooms[i][0])
            )
            # if not configExists(newRooms, hallway, closed):
            if not closed.get(newState):
                moves.append(newState)
            hallway[j] = None

    return moves


def numSolved(config):
    solved = 0
    for r in range(len(config.rooms)):
        for a in reversed(config.rooms[r]):
            if roomHash(a) == r:
                solved += 1
            else:
                break
    return solved


def printConfig(e, depth=2):
    print("#############")
    print("#", end="")
    for h in e.hallway:
        if h is None:
            print(".", end="")
        else:
            print(h[0], end="")
    print("#")

    rooms = copy.deepcopy(e.rooms)
    for r in range(len(rooms)):
        while len(rooms[r]) < depth:
            rooms[r].insert(0, ".")

    for i in range(depth):
        if i == 0:
            print("##", end="")
        else:
            print("  ", end="")

        for r in rooms:
            print("#" + r[i][0], end="")

        if i == 0:
            print("###")
        else:
            print("#  ")
    print("  #########")
    print()


def dijkstra(firstState, depth=2):
    openSet = PriorityQueue()
    openSet.put(firstState)
    closed = {}
    seen = {firstState: firstState}
    passes = 0
    while True:
        # while True:
        #     lowest = openSet.get()
        #     if lowest.cost != seen[lowest].cost:
        #         lowest.cost = seen[lowest].cost
        #         openSet.put(lowest)
        #     else:
        #         break
        lowest = openSet.get()

        passes += 1
        if passes % 500 == 0:
            os.system("clear")
            printConfig(lowest, depth)
            print(passes)
        # print(len(openSet))
        allDone = True
        for r in range(4):
            if not (
                len(lowest.rooms[r]) == depth and roomSatisfied(lowest.rooms[r], r)
            ):
                allDone = False
        if allDone:
            print("First: %d" % (lowest.cost))
            break

        updates = move(lowest.rooms, lowest.hallway, closed, depth)
        for e in updates:
            e.cost += lowest.cost
            # if e.cost > 12550:
            #     continue
            try:
                neighbourState = seen[e]
                if neighbourState.cost > e.cost:
                    neighbourState.parent = lowest
                    neighbourState.cost = e.cost
            except KeyError:
                e.parent = lowest
                seen[e] = e
                openSet.put(seen[e])
        closed[lowest] = lowest

    ogLowest = lowest
    while lowest is not None:
        printConfig(lowest, depth)
        print(lowest.cost)
        lowest = lowest.parent
    return ogLowest


rooms = [[], [], [], []]
hallway = [None for i in range(11)]

for i in range(2, len(lines) - 1):
    for j in range(4):
        rooms[j].append((lines[i][3 + (2 * j)]) + str(i * 10 + j))

firstState = BurrowState(rooms, hallway, 0)

print("First: %d" % (dijkstra(firstState).cost))
input()

toAppend = [["D40", "D41"], ["C40", "B40"], ["B41", "A40"], ["A41", "C41"]]
# toAppend = [["A40", "A41"], ["B40", "B40"], ["C41", "C40"], ["D41", "D41"]]
for r in range(len(rooms)):
    last = rooms[r][-1]
    rooms[r] = [rooms[r][0]]
    rooms[r].extend(toAppend[r])
    rooms[r].append(last)

firstState = BurrowState(rooms, hallway, 0)
print("Second: %d" % (dijkstra(firstState, 4).cost))
