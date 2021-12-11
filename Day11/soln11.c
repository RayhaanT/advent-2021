#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringUtils.h"
#include "fileUtils.h"

#define STEPS 100
#define ADJACENTS 8

struct Octopus {
    int energy;
    struct Octopus ** neighbours;
    int flashed;
}; typedef struct Octopus Octopus;

void generateAdjacents(Octopus * o, Octopus ** grid, int y, int x, int height, int width) {
    for(int i = 0; i < ADJACENTS; i++)
        o->neighbours[i] = NULL;
    int left = x > 0;
    int right = x < width - 1;
    int down = y < width - 1;
    int up = y > 0;

    if(left)
        o->neighbours[0] = &grid[y][x - 1];
    if(right)
        o->neighbours[1] = &grid[y][x + 1];
    if(up)
        o->neighbours[2] = &grid[y - 1][x];
    if(down)
        o->neighbours[3] = &grid[y + 1][x];
    if(left && up)
        o->neighbours[4] = &grid[y - 1][x - 1];
    if(left && down)
        o->neighbours[5] = &grid[y + 1][x - 1];
    if(right && up)
        o->neighbours[6] = &grid[y - 1][x + 1];
    if(right && down)
        o->neighbours[7] = &grid[y + 1][x + 1];
}

int flash(Octopus * o, int chain) {
    if (chain && !o->flashed) {
        o->energy++;
    }
    if (o->energy < 10) {
        return 0;
    }
    o->flashed = 1;
    int flashes = 1;
    o->energy = 0;
    for(int i = 0; i < ADJACENTS; i++) {
        if (o->neighbours[i]) {
            flashes += flash(o->neighbours[i], 1);
        }
    }
    return flashes;
}

Octopus octopus(int energy) {
    Octopus o;
    o.energy = energy;
    o.neighbours = malloc(ADJACENTS * sizeof(Octopus));
    o.flashed = 0;
    return o;
}

void print(Octopus ** octopi) {
    for(int y = 0; y < 10; y++) {
        for(int x = 0; x < 10; x++) {
            printf("%d", octopi[y][x].energy);
        }
        printf("\n");
    }
    printf("\n");
}

int allFlashed(Octopus ** octopi, int height, int width) {
    int allOctopi = height*width;
    int flashed = 0;
    for(int y = 0; y < height; y++) {
        for(int x = 0; x < height; x++) {
            flashed += octopi[y][x].flashed;
        }
    }
    return flashed == allOctopi;
}

int main() {
    int fileSize;
    char ** lines = getInputLines(11, &fileSize);

    int len = strlen(lines[0]);
    Octopus ** octopi = malloc(fileSize * sizeof(Octopus *));

    for(int y = 0; y < fileSize; y++) {
        octopi[y] = malloc(len * sizeof(Octopus));
        for(int x = 0; x < len; x++) {
            Octopus newOctopus = octopus(lines[y][x] - '0');
            octopi[y][x] = newOctopus;
        }
    }

    for(int y = 0; y < fileSize; y++) {
        for(int x = 0; x < fileSize; x++) {
            generateAdjacents(&octopi[y][x], octopi, y, x, fileSize, len);
        }
    }

    int totalFlashes = 0;
    int stepFlashes = 0;
    int counter = 0;
    int done = 0;
    int finalCounter = 0;
    while(!done || counter < STEPS) {
        for(int y = 0; y < fileSize; y++) {
            for(int x = 0; x < fileSize; x++) {
                octopi[y][x].energy++;
                octopi[y][x].flashed = 0;
            }
        }

        int stepFlashes = 0;
        for(int y = 0; y < fileSize; y++) {
            for(int x = 0; x < fileSize; x++) {
                stepFlashes += flash(&octopi[y][x], 0);
            }
        }
        if (counter < STEPS) {
            totalFlashes += stepFlashes;
        }

        counter++;
        if (!done) {
            done = allFlashed(octopi, fileSize, len);
            finalCounter = counter;
        }
    }

    printf("First: %d\n", totalFlashes);
    printf("Second: %d\n", finalCounter);
}
