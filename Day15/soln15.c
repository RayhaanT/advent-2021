#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringUtils.h"
#include "fileUtils.h"
#include <stdbool.h>
#include <math.h>

struct Point {
    int risk;
    int x;
    int y;
    int cost;
    struct Point * parent;
    struct Point ** neighbours;
}; typedef struct Point Point;

void generateNeighbours(Point * p, Point ** grid, int height, int width, int x, int y) {
    for(int i = 0; i < 4; i++)
        p->neighbours[i] = NULL;

    if (x > 0)
        p->neighbours[0] = &grid[y][x - 1];
    if (x < width - 1)
        p->neighbours[1] = &grid[y][x + 1];
    if (y > 0)
        p->neighbours[2] = &grid[y - 1][x];
    if (y < height - 1)
        p->neighbours[3] = &grid[y + 1][x];
}

Point point(int risk, int x, int y) {
    Point p = {risk, x, y, -1, NULL, malloc(4 * sizeof(Point *))};
    return p;
}

bool isVisited(Point p, bool * visited, int width) {
    if (visited[p.x + (width * p.y)]) {
        return true;
    }
    return false;
}

void visit(Point p, bool * visited, int width) {
    visited[p.x + (width * p.y)] = true;
}

int heuristic(Point p, int height, int width) {
    return sqrt(pow((p.x - width), 2) + pow((p.y - height), 2));
}

int score(Point p, int height, int width) {
    return p.cost + heuristic(p, height, width);
}

void openSetInsert(Point *p, Point ** openSet, int size) {
    for(int i = 0; i < size; i++) {
        if (openSet[i] == p) {
            return;
        }
        if (!openSet[i]) {
            openSet[i] = p;
            return;
        }
    }
}

void openSetRemove(Point *p, Point ** openSet, int size) {
    int critical = 0;
    for(int i = 0; i < size; i++) {
        if(openSet[i] == p) {
            critical = i;
            openSet[i] = NULL;
            break;
        }
    }

    for(int i = critical; i < size - 1; i++) {
        openSet[i] = openSet[i + 1];
    }
    openSet[size - 1] = NULL;
}

bool openExists(Point *p, Point ** set, int size) {
    for(int i = 0; i < size; i++) {
        if (p == set[i]) {
            return true;
        }
    }
    return false;
}

void printOpenSet(Point ** plane, Point ** openSet, int height, int width, bool * visited) {
    for(int y = 0; y < height; y++) {
        for(int x = 0; x <width; x++) {
            if(openExists(&plane[y][x], openSet, height * width)) {
                printf("%d", plane[y][x].risk);
            }
            else if (isVisited(plane[y][x], visited, width)) {
                printf("x");
            }
            else {
                printf(" ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

int main() {
    int height;
    char ** lines = getInputLines(15, &height);
    int width = strlen(lines[0]);

    Point ** plane = malloc(height * sizeof(Point *));

    for(int y = 0; y < height; y++) {
        plane[y] = malloc(width * sizeof(Point));
        for(int x = 0; x < width; x++) {
            plane[y][x] = point(lines[y][x] - '0', x, y);
        }
    }

    for(int y = 0; y < height; y++) {
        for(int x = 0; x < strlen(lines[y]); x++) {
            generateNeighbours(&plane[y][x], plane, height, width, x, y);
        }
    }

    Point *current = &plane[0][0];
    bool * visited = malloc(width * height * sizeof(bool));
    Point ** openSet = malloc(width * height * sizeof(Point *));
    for(int i = 0; i < width * height; i++) {
        visited[i] = false;
        openSet[i] = NULL;
    }

    openSet[0] = current;
    Point *end = &plane[height - 1][width - 1];
    while (current != end) {
        bool first = true;
        int comp = 0;
        for(int i = 0; i < width * height; i++) {
            if (!openSet[i]) {
                break;
            }
            if (first) {
                current = openSet[i];
                first = false;
                comp = score(*current, height, width);
                continue;
            }
            if (score(*openSet[i], height, width) < comp) {
                current = openSet[i];
                comp = score(*current, height, width);
            }
        }

        if (current == end) {
            break;
        }

        //printf("x: %d y: %d r: %d c: %d\n", current->x, current->y, current->risk, current->cost);

        openSetRemove(current, openSet, width * height);
        visit(*current, visited, width);

        for(int i = 0; i < 4; i++) {
            if (!current->neighbours[i])
                continue;

            Point *n = current->neighbours[i];
            if (!isVisited(*n, visited, width)) {
                int tentative = current->cost + n->risk;
                if (tentative < n->cost || n->cost == -1) {
                    n->cost = tentative;
                    n->parent = current;
                }
                openSetInsert(n, openSet, width * height);
            }
        }
        // printOpenSet(plane, openSet, height, width, visited);
    }

    current = end;
    int total = 0;
    while (current->parent) {
        total += current->risk;
        current = current->parent;
        printf("x: %d y: %d r: %d\n", current->x, current->y, current->risk);
    }
    printf("Solution: %d\n", total);
}
