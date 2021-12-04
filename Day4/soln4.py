from dataclasses import dataclass

inFile = open('../inputs/Day4.txt')
lines = inFile.readlines()

class Square:
  def __init__(self, num, state, row):
    self.num = num
    self.state = state
    self.row = row

draws = lines[0].strip().split(',')
for d in range(0, len(draws)):
    draws[d] = int(draws[d])

boards = []

def checkRow(board, row):
    for s in board[row]:
        if s.state == False:
            return False
    return True

def checkCol(board, col):
    for r in board:
        if r[col].state == False:
            return False
    return True
    

del lines[0]
del lines[0]
newBoard = []
for l in lines:
    if(l == '\n'):
        boards.append(newBoard)
        newBoard = []
        continue

    row = l.strip().split()
    squares = []
    for r in range(0, len(row)):
        squares.append(Square(int(row[r]), False, len(newBoard)))
    newBoard.append(squares)

boards.append(newBoard)

def sumRow(row):
    total = 0
    for s in row:
        if s.state == False:
            total += s.num
    return total

def sumCol(board, col):
    total = 0
    for r in baord:
        if r[col].state == False:
            total += r[col].num
    return total

def sumBoard(board):
    total = 0
    for r in board:
        total += sumRow(r)
    return total

def helper(draws, boards):
    for d in draws:
        for b in boards:
            for row in b:
                for r in range(0, len(row)):
                    if row[r].num == d:
                        row[r].state = True
                        if checkRow(b, row[r].row):
                            print("First: " + str(sumBoard(b) * d))
                            return
                        if checkCol(b, r):
                            print("First: " + str(sumBoard(b) * d))
                            return

helper(draws, boards)

def helper2(draws, boards):
    for d in draws:
        length = len(boards)
        deleted = 0
        for b in range(0, length):
            for r in boards[b - deleted]:
                for s in range(0, len(r)):
                    if r[s].num == d:
                        r[s].state = True
                        if checkRow(boards[b - deleted], r[s].row) or checkCol(boards[b - deleted], s):
                            if len(boards) == 1:
                                print("Second: " + str(sumBoard(boards[0]) * d))
                                return
                            del boards[b - deleted]
                            deleted += 1

# Reset for part 2
for b in boards:
    for r in b:
        for s in range(0, len(r)):
            r[s].state = False

helper2(draws, boards)
