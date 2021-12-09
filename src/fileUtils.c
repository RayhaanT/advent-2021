#include "fileUtils.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#define INPUT_PATH "inputs/Day"
#define INPUT_SUFFIX ".txt"
#define test "3"

char * getFilePath(int day) {
    int length = (int)((ceil(log10(day))+1)*sizeof(char)) + strlen(INPUT_PATH);
    char *path = (char *) malloc(length * sizeof(char));
    sprintf(path, "%s%d%s", INPUT_PATH, day, INPUT_SUFFIX);
    return path;
}

FILE * getInput(int day) {
    FILE *input;
    char *path = getFilePath(day);
    input = fopen(path, "r");
    return input;
}

size_t maxLineBufferSize(FILE * input) {
    ssize_t read;
    char * line = NULL;
    size_t len = 0;

    size_t max = 0;
    while ((read = getline(&line, &len, input)) != -1) {
        if (len > max) {
            max = len;
        }
    }
    rewind(input);

    return max;
}

char ** getInputLines(int day, int *size) {
    int sz = getFileSize(day);
    *size = sz;

    FILE *input = getInput(day);

    char **lines = malloc(sz * sizeof(char*));
    size_t strSize = maxLineBufferSize(input);

    for(int i = 0; i < sz; i++) {
        lines[i] = malloc(strSize);
    }

    ssize_t read;
    char * line = NULL;
    size_t len = 0;

    int index = 0;
    while ((read = getline(&line, &len, input)) != -1) {
        if(line[read - 1] == '\n') {
            line[read - 1] = '\0';
        }
        strcpy(lines[index], line);
        index++;
    }
    fclose(input);

    return lines;
}

int getFileSize(int day) {
    FILE *file = getInput(day);

    int lines = 0;
    int ch = 0;
    while(!feof(file)) {
        ch = fgetc(file);
        if(ch == '\n') {
            lines++;
        }
    }

    fclose(file);

    return lines;
}

int intComparator (const void * aP, const void * bP) {
    int a = *((int*)aP);
    int b = *((int*)bP);
    if (a > b) return  1;
    if (b < a) return -1;
    return 0;
}
