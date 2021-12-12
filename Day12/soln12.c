#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringUtils.h"
#include "fileUtils.h"
#include <stdbool.h>
#include <ctype.h>

struct Cave {
    bool small;
    struct Cave ** neighbours;
    int neighbourNum;
    char * id;
    int visited;
}; typedef struct Cave Cave;

Cave cave(char * id, int potentialPaths) {
    bool small = islower(id[0]) ? true : false;
    Cave ** placeholder = malloc(potentialPaths * sizeof(Cave *));
    for(int i = 0; i < potentialPaths; i++) {
        placeholder[i] = NULL;
    }
    Cave c = {
        small,
        placeholder,
        0,
        id,
        0
    };
    return c;
}

void parsePath(char * firstId, char * secondId, Cave * caves, int size) {
    Cave * first = NULL;
    Cave * second = NULL;

    for(int i = 0; i < size; i++) {
        if (strcmp(caves[i].id, firstId) == 0) {
            first = &caves[i];
        }
        if (strcmp(caves[i].id, secondId) == 0) {
            second = &caves[i];
        }
    }

    first->neighbours[first->neighbourNum] = second;
    second->neighbours[second->neighbourNum] = first;
    first->neighbourNum++;
    second->neighbourNum++;
}

int probe(Cave * root, bool first, Cave * doubling, bool allowSeconds) {
    if (strcmp(root->id, "end") == 0) {
        if (allowSeconds) {
            if (doubling->visited == 2)
                return 1;
            return 0;
        }
        return 1;
    }
    if (strcmp(root->id, "start") == 0 && !first)
        return 0;
    if (root->visited == 2)
        return 0;
    if (root->visited == 1 && root != doubling)
        return 0;
    if (root->small)
        root->visited++;

    int paths = 0;
    for(int i = 0; i < root->neighbourNum; i++) {
        paths += probe(root->neighbours[i], false, doubling, allowSeconds);
    }
    root->visited--;
    return paths;
}

Cave * getCave(Cave * caves, int len, char * key) {
    for(int i = 0; i < len; i++) {
        if (strcmp(caves[i].id, key) == 0)
            return &caves[i];
    }
    return NULL;
}

int main() {
    int fileSize;
    char ** lines = getInputLines(12, &fileSize);

    char ** caveIds = malloc(fileSize * 2 * sizeof(char *));
    int caveIndex = 0;
    for(int i = 0; i < fileSize; i++) {
        int len;
        char ** split = splitString(lines[i], "-", &len);
        caveIds[caveIndex] = split[0];
        caveIds[caveIndex + 1] = split[1];
        caveIndex += 2;
    }
    char ** sortedIds = malloc(fileSize * 2 * sizeof(char *));
    memcpy(sortedIds, caveIds, sizeof(char *) * fileSize * 2);
    qsort(sortedIds, fileSize * 2, sizeof(char *), stringComparator);

    char *last = NULL;
    int uniques = 0;
    char ** uniqueIds = malloc(fileSize * 2 * sizeof(char *));
    for(int i = 0; i < fileSize * 2; i++) {
        if (!last) {
            last = sortedIds[i];
            uniqueIds[uniques] = sortedIds[i];
            uniques++;
            continue;
        }
        if (strcmp(last, sortedIds[i]) != 0) {
            last = sortedIds[i];
            uniqueIds[uniques] = sortedIds[i];
            uniques++;
        }
    }
    for(int i = uniques; i < fileSize * 2; i++) {
        uniqueIds[i] = NULL;
    }

    Cave * caves = malloc(uniques * sizeof(Cave));
    for(int i = 0; i < uniques; i++) {
        caves[i] = cave(uniqueIds[i], uniques - 1);
    }

    for(int i = 0; i < fileSize * 2; i+=2) {
        parsePath(caveIds[i], caveIds[i + 1], caves, uniques);
    }

    Cave * start = getCave(caves, uniques, "start");
    int paths = probe(start, true, NULL, false);
    printf("First: %d\n", paths);
    
    for(int i = 0; i < uniques; i++) {
        paths += probe(start, true, &caves[i], true);
    }
    printf("Second: %d\n", paths);
}
