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

def sumBoard(board):
    total = 0
    for r in board:
        total += sumRow(r)
    return total

def playBingo(draws, boards):
    first = True
    for d in draws:
        length = len(boards)
        deleted = 0
        for b in range(0, length):
            ind = b - deleted # Prevent out of range after deleting solved boards
            for r in boards[ind]:
                for s in range(0, len(r)):
                    if r[s].num == d:
                        r[s].state = True
                        if checkRow(boards[ind], r[s].row) or checkCol(boards[ind], s):
                            if first:
                                print("First: " + str(sumBoard(boards[ind]) * d))
                                first = False
                            if len(boards) == 1:
                                print("Second: " + str(sumBoard(boards[ind]) * d))
                                return
                            del boards[ind]
                            deleted += 1

playBingo(draws, boards)
