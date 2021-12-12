#include <stdio.h>
#include <stdlib.h>
#include "stringUtils.h"
#include "fileUtils.h"
#include "stdbool.h"
#include <string.h>
#include <math.h>

struct Point {
    int x;
    int y;
    int height;
    int basinSize;
    struct Point * drainage;
    struct Point ** neighbours;
    bool visited;
};
typedef struct Point Point;

int * getHeights(char * line, int * length) {
    int len = strlen(line);
    *length = len;

    int * heights = malloc(len * sizeof(int));
    for(int i = 0; i < len; i++) {
        heights[i] = line[i] - '0';
    }

    return heights;
}

Point constructPoint(int x, int y, int height) {
    Point p = {x, y, height, 0, NULL, malloc(4 * sizeof(Point *)), false};
    return p;
}

void generateAdjacents(Point * p, Point ** grid, int height, int width) {
    int x = p->x; int y = p->y;
    for(int i = 0; i < 4; i++)
        p->neighbours[i] = NULL;

    if(x > 0)
        p->neighbours[0] = &grid[y][x - 1];
    if(x < width - 1)
        p->neighbours[1] = &grid[y][x + 1];
    if(y > 0)
        p->neighbours[2] = &grid[y - 1][x];
    if(y < height - 1)
        p->neighbours[3] = &grid[y + 1][x];
}

bool isLocalMin(const Point p) {
    for(int i = 0; i < 4; i++) {
        if(!p.neighbours[i]) {
            continue;
        }
        if(p.neighbours[i]->height <= p.height) {
            Point n = *p.neighbours[i];
            return false;
        };
    }
    return true;
}

Point * probeBasin(Point * point) {
    if(isLocalMin(*point))
        return point;
    if(point->drainage)
        return point->drainage;
    if(point->height == 9) {
        return NULL;
    }
    
    point->visited = true;
    Point *endpoint = NULL;

    for(int i = 0; i < 4; i++) {
        if(!point->neighbours[i]) {
            continue;
        }
        if(point->neighbours[i]->height <= point->height && !point->neighbours[i]->visited) {
            if(!endpoint) {
                endpoint = probeBasin(point->neighbours[i]);
            }
            else {
                Point *newEndpoint = probeBasin(point->neighbours[i]);
                if(newEndpoint != endpoint) {
                    point->visited = false;
                    return NULL;
                }
            }
        }
    }

    point->drainage = endpoint;
    point->visited = false;
    return endpoint;
}

int propogate(Point * point) {
    if(point->height == 9 || point->visited)
        return 0;

    int basinSize = 1;
    point->visited = true;
    for(int i = 0; i < 4; i++) {
        if(!point->neighbours[i]) {
            continue;
        }
        basinSize += propogate(point->neighbours[i]);
    }
    return basinSize;
}

int main() {
    int height;
    char ** lines = getInputLines(9, &height);

    int width = 0;
    Point ** grid = malloc(height * sizeof(Point *));
    for(int i = 0; i < height; i++) {
        int * heights = getHeights(lines[i], &width);
        grid[i] = malloc(width * sizeof(Point));

        for(int h = 0; h < width; h++) {
            grid[i][h] = constructPoint(h, i, heights[h]);
        }
    }

    for(int y = 0; y < height; y++) {
        for(int x = 0; x < width; x++) {
            generateAdjacents(&grid[y][x], grid, height, width);
        }
    }

    // This also works under the assumption that you could get points
    // not equal to 9 and not in basins. Due to input specification this
    // is not necessary and we can just branch from the lowpoints
    /*for(int y = 0; y < height; y++) {
        for(int x = 0; x < width; x++) {
            Point *endpoint = probeBasin(&grid[y][x]);
            if(endpoint) {
                endpoint->basinSize++;
            }
        }
    }*/

    int lowPoints = 0;
    int largest[] = {0, 0, 0};
    for(int y = 0; y < height; y++) {
        for(int x = 0; x < width; x++) {
            if(isLocalMin(grid[y][x])) {
                lowPoints += grid[y][x].height + 1;

                // The more robust solution comments out this line
                // and uncomments the above block. Not necessary given
                // input spec of this problem
                grid[y][x].basinSize = propogate(&grid[y][x]);

                if(grid[y][x].basinSize > largest[0]) {
                    largest[0] = grid[y][x].basinSize;
                    qsort(largest, 3, sizeof(int), intComparator);
                }
            }
        }
    }

    printf("First: %d\n", lowPoints);
    printf("Second: %d\n", largest[0] * largest[1] * largest[2]);

    return 0;
}
