#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringUtils.h"
#include "fileUtils.h"

#define min(a,b) \
    ({ __typeof__ (a) _a = (a); \
        __typeof__ (b) _b = (b); \
        _a < _b ? _a : _b; })

int * parsePoint(char * line) {
    int size;
    int * arr = stringToIntArr(line, ",", &size);
    return arr;
}

int * parseInstruction(char * line) {
    int size;
    char ** arr = splitString(line, " ", &size);
    char * axis = arr[2];
    char ** components = splitString(axis, "=", &size);

    int * data = malloc(2 * sizeof(int));
    data[0] = stringToInt(components[1]);
    data[1] = strcmp(components[0], "y");
    return data;
}

void foldVert(int ** paper, int width, int height, int row) {
    int mirrorEdge = min(2 * row + 1, height);
    for(int x = 0; x < width; x++) {
        for(int y = 1; row + y < mirrorEdge; y++) {
            paper[row - y][x] += paper[row + y][x];
        }
    }
}

void foldHorz(int ** paper, int width, int height, int col) {
    int mirrorEdge = min(2 * col + 1, width);
    for(int y = 0; y < height; y++) {
        for(int x = 1; col + x < mirrorEdge; x++) {
            paper[y][col - x] += paper[y][col + x];
        }
    }
}

int count(int ** paper, int width, int height) {
    int total = 0;
    for(int y = 0; y < height; y++) {
        for(int x = 0; x < width; x++) {
            if (paper[y][x]) {
                total++;
            }
        }
    }
    return total;
}

void print(int ** paper, int width, int height) {
    for(int y = 0; y < height; y++) {
        for(int x = 0; x < width; x++) {
            if(paper[y][x]) {
                printf("#");
            }
            else {
                printf(".");
            }
        }
        printf("\n");
    }
    printf("\n");
}

int main() {
    int fileSize;
    char ** lines = getInputLines(13, &fileSize);

    int maxX = 0;
    int maxY = 0;
    int firstInstructionIndex = 0;
    int ** coords = malloc(fileSize * sizeof(int *));
    for(int i = 0; i < fileSize; i++) {
        if (strlen(lines[i]) < 2) {
            firstInstructionIndex = i + 1;
            break;
        }
        coords[i] = parsePoint(lines[i]);
        if (coords[i][0] > maxX)
            maxX = coords[i][0];
        if (coords[i][1] > maxY)
            maxY = coords[i][1];
    }
    maxX++;
    maxY++;

    int ** paper = malloc(maxY * sizeof(int *));
    for(int i = 0; i < maxY; i++) {
        paper[i] = malloc(maxX * sizeof(int));
        for(int j = 0; j < maxX; j++) {
            paper[i][j] = 0;
        }
    }
    for(int i = 0; i < firstInstructionIndex - 1; i++) {
        paper[coords[i][1]][coords[i][0]] = 1;
    }

    int height = maxY;
    int width = maxX;
    for(int i = firstInstructionIndex; i < fileSize; i++) {
        int * instruction = parseInstruction(lines[i]);
        if (instruction[1]) {
            foldHorz(paper, width, height, instruction[0]);
            width = instruction[0];
        }
        else {
            foldVert(paper, width, height, instruction[0]);
            height = instruction[0];
        }
        if (i == firstInstructionIndex) {
            printf("First: %d\n", count(paper, width, height));
        }
        //print(paper, width, height);
    }

    printf("Second:\n");
    print(paper, width, height);

    return 0;
}
