#include <stdio.h>
#include "fileUtils.h"
#include "stringUtils.h"
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdbool.h>

#define max(a,b) \
    ({ __typeof__ (a) _a = (a); \
        __typeof__ (b) _b = (b); \
        _a > _b ? _a : _b; })

struct Coord {
    int x;
    int y;
};
typedef struct Coord Coord;

struct Vent {
    Coord start;
    Coord end;
    Coord slope;
    bool linear;
};
typedef struct Vent Vent;

Coord constructCoord(int x, int y) {
    Coord c = {x, y};
    return c;
}

Vent constructVent(Coord start, Coord end) {
    Vent v;
    v.start = start;
    v.end = end;

    int dx = end.x - start.x;
    int dy = end.y - start.y;
    int xSlope = (dx > 0) ? 1 : ((dx < 0) ? -1 : 0);
    int ySlope = (dy > 0) ? 1 : ((dy < 0) ? -1 : 0);

    v.slope = constructCoord(xSlope, ySlope);
    v.linear = true;
    if(xSlope != 0 && ySlope != 0) {
        v.linear = false;
    }

    return v;
}

Coord add(const Coord a, const Coord b) {
    Coord out = {a.x + b.x, a.y + b.y};
    return out;
}

bool equals(const Coord a, const Coord b) {
    return a.x == b.x && a.y == b.y;
}

Vent parseVent(char * in) {
    ssize_t len = strlen(in);

    int size;
    char ** blocks = splitString(in, " ", &size);

    int * start = stringToIntArr(blocks[0], ",", &size);
    int * end = stringToIntArr(blocks[2], ",", &size);

    return constructVent(constructCoord(start[0], start[1]), constructCoord(end[0], end[1]));
}

void mark(int ** grid, const Coord index) {
    grid[index.y][index.x]++;
}

int main() {
    int fileLength;
    char ** lines = getInputLines(5, &fileLength);

    Vent *vents = (Vent *) malloc(fileLength * sizeof(Vent));

    int maxX = 0;
    int maxY = 0;
    for(int i = 0; i < fileLength; i++) {
        vents[i] = parseVent(lines[i]);

        int mx = max(vents[i].start.x, vents[i].end.x);
        int my = max(vents[i].start.y, vents[i].end.y);
        maxX = max(maxX, mx);
        maxY = max(maxY, my);
    }

    maxX++; maxY++;

    int ** grid = malloc(maxY * sizeof(int *));
    for(int y = 0; y < maxY; y++) {
        grid[y] = malloc(maxX * sizeof(int));
        for(int x = 0; x < maxX; x++) 
            grid[y][x] = 0;
    }

    for(int i = 0; i < fileLength; i++) {
        // Uncomment this block for answer 1. Leave commented for 2
        // if(!vents[i].linear)
        //    continue;
       
        Coord stepper = vents[i].start;
        do {
            mark(grid, stepper);
            stepper = add(stepper, vents[i].slope);
        } while(!equals(stepper, vents[i].end));
        mark(grid, vents[i].end);
    }

    int total = 0;
    for(int y = 0; y < maxY; y++)
        for(int x = 0; x < maxX; x++)
            if(grid[y][x] > 1)
                total++;

    printf("Total: %d\n", total);
    printf("See file and comment/uncomment to switch answer output\n");

    return 0;
}
