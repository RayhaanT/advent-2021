#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "stringUtils.h"
#include "fileUtils.h"

struct Chunk {
    char open;
    char closer;
    bool closed;
    struct Chunk * child;
    struct Chunk * parent;
};
typedef struct Chunk Chunk;

char closers[] = {')', ']', '}', '>'};
int corruptionScores[] = {3, 57, 1197, 25137};
int incompleteScores[] = {1, 2, 3, 4};

int hash(const char in) {
    switch (in) {
        case '(': return 0;
        case '[': return 1;
        case '{': return 2;
        case '<': return 3;
        default: return -1;
    }
}

int backHash(const char in) {
    switch (in) {
        case ')': return 0;
        case ']': return 1;
        case '}': return 2;
        case '>': return 3;
        default: return -1;
    }
}

bool close(Chunk * closeCandidate, char closer) {
    if(closer == closeCandidate->closer) {
        closeCandidate->closed = true;
        return true;
    }
    return false;
}

Chunk chunk(const char start, Chunk * parent) {
    Chunk c = {start, closers[hash(start)], false, NULL, parent};
    return c;
}

int main() {
    int fileSize;
    char ** lines = getInputLines(10, &fileSize);

    int corruptionScore = 0;
    long * autocompleteScores = (long *) malloc(fileSize * sizeof(long));

    for(int l = 0; l < fileSize; l++) {
        char * line = lines[l];
        size_t len = strlen(line);

        bool corrupted = false;
        Chunk * currentChunk = NULL;

        for(int c = 0; c < len; c++) {
            if(hash(line[c]) == -1) {
                bool success = close(currentChunk, line[c]);
                if (success) {
                    currentChunk = currentChunk->parent;
                    if(currentChunk) {
                        free(currentChunk->child);
                    }
                }
                else {
                    corrupted = true;
                    corruptionScore += corruptionScores[backHash(line[c])];
                    break;
                }
            }
            else {
                Chunk * newChunk = malloc(sizeof(Chunk));
                *newChunk = chunk(line[c], currentChunk);
                if(currentChunk) {
                    currentChunk->child = newChunk;
                }
                currentChunk = newChunk;
            }
        }

        if(!corrupted && currentChunk) {
            long autoScore = 0;
            while(currentChunk->parent != NULL) {
                autoScore *= 5;
                autoScore += incompleteScores[hash(currentChunk->open)];
                currentChunk = currentChunk->parent;
            }
            autoScore *= 5;
            autoScore += incompleteScores[hash(currentChunk->open)];
            autocompleteScores[l] = autoScore;
        }
        else {
            autocompleteScores[l] = 0; 
        }
    }

    printf("First: %d\n", corruptionScore);
    qsort(autocompleteScores, fileSize, sizeof(long), longComparator);

    int offset = 0;
    for(int i = 0; i < fileSize; i++) {
        if(autocompleteScores[i] < 1) {
            offset++;
        }
    }
    long * filteredScores = autocompleteScores + offset;
    int middleIndex = (fileSize - offset - 1)/2;
    printf("Second: %ld\n", filteredScores[middleIndex]);
}
