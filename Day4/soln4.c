#include <stdio.h>
#include "fileUtils.h"
#include "stringUtils.h"
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdbool.h>

#define BOARD_SIDE_LENGTH 5

struct Square {
    int val;
    bool marked;
};
typedef struct Square Square;

struct Board {
    Square **grid;
    bool won;
};
typedef struct Board Board;

Square * genRow(char * row) {
    int length;
    int * vals = stringToIntArr(row, " ", &length);
    Square * squares = (Square *) malloc(length * sizeof(Square));

    for(int i = 0; i < length; i++) {
        squares[i].val = vals[i];
        squares[i].marked = false;
    }

    return squares;
}

bool checkRow(Square * row) {
    for(int i = 0; i < BOARD_SIDE_LENGTH; i++) {
        if(!row[i].marked) {
            return false;
        }
    }
    return true;
}

bool checkCol(Square ** grid, int col) {
    for(int i = 0; i < BOARD_SIDE_LENGTH; i++) {
        if(!grid[i][col].marked) {
            return false;
        }
    }
    return true;
}

bool won(Board * b) {
    for(int i = 0; i < BOARD_SIDE_LENGTH; i++) {
        if(checkRow(b->grid[i]) || checkCol(b->grid, i)) {
            b->won = true;
            return true;
        }
    }
    return false;
}

void mark(Board * b, int val) {
    for(int x = 0; x < BOARD_SIDE_LENGTH; x++) {
        for(int y = 0; y < BOARD_SIDE_LENGTH; y++) {
            if(b->grid[x][y].val == val) {
                b->grid[x][y].marked = true;
            }
        }
    }
}

int sumBoard(const Board b) {
    int total = 0;
    for(int x = 0; x < BOARD_SIDE_LENGTH; x++) {
        for(int y = 0; y < BOARD_SIDE_LENGTH; y++) {
            if(!b.grid[x][y].marked) {
                total += b.grid[x][y].val;
            }
        }
    }
    return total;
}

bool lastBoard(const Board * boards, int length) {
    for(int i = 0; i < length; i++) {
        if(!boards[i].won) {
            return false;
        }
    }
    return true;
}

void playBingo(Board * boards, int * draws, int boardNum, int length) {
    bool first = true;
    for(int i = 0; i < length; i++) {
        for(int b = 0; b < boardNum; b++) {
            if(boards[b].won) {
                continue;
            }

            mark(&boards[b], draws[i]);

            if(won(&boards[b])) {
                if(first) {
                    int sum = sumBoard(boards[b]);
                    printf("First: %d\n", sum * draws[i]);
                    first = false;
                }
                if(lastBoard(boards, boardNum)) {
                    printf("Second: %d\n", sumBoard(boards[b]) * draws[i]);
                    return;
                }
            }
        }
    }
}

int main() {
    int length;
    char ** lines = getInputLines(4, &length);
    int fileLength = length;
    int boardNum = ceil((float)(length - 2)/6);

    int *draws = stringToIntArr(lines[0], ",", &length);

    char *newline = lines[1];

    Board *boards = (Board *) malloc(boardNum * sizeof(Board));
    for(int b = 0; b < boardNum; b++) {
        boards[b].grid = malloc(BOARD_SIDE_LENGTH * sizeof(Square *));
        boards[b].won = false;
        for(int i = 0; i < BOARD_SIDE_LENGTH; i++) {
            boards[b].grid[i] = malloc(BOARD_SIDE_LENGTH * sizeof(Square));
        }
    }

    int boardIndex = 0;
    int rowIndex = 0;
    for(int i = 2; i < fileLength; i++) {
        if(strcmp(lines[i], newline) == 0) {
            rowIndex = 0;
            boardIndex++;
        }
        else {
            boards[boardIndex].grid[rowIndex] = genRow(lines[i]);
            rowIndex++;
        }
    }

    playBingo(boards, draws, boardNum, length);
    return 0;
}
