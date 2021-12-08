#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringUtils.h"

int stringToInt(char * input) {
    char *end;
    return strtol(input, &end, 10);
}

size_t postSplitSize(char * input, const char * delim) {
    char *token;
    size_t size = 0;

    char *counter = NULL;
    counter = strdup(input);
    token = strtok(counter, delim);

    while (token != NULL) {
        size++;
        token = strtok(NULL, delim);
    }

    return size;
}

int * stringToIntArr(char * input, const char * delim, int * length) {
    char * token;
    size_t size = postSplitSize(input, delim);
    *length = size;

    int * output = (int *) malloc(size * sizeof(int));
    int index = 0;
    token = strtok(input, delim);
    while (token != NULL) {
        output[index] = stringToInt(token);
        index++;
        token = strtok (NULL, delim);
    }

    return output;
}

char ** splitString(char * input, const char * delim, int * length) {
    size_t size = postSplitSize(input, delim);
    *length = size;

    char ** array = malloc(size * sizeof(char *));

    char *token = strtok(input, delim);

    int i = 0;
    while (token != NULL) {
        array[i++] = token;
        token = strtok (NULL, delim);
    }

    return array;
}

int deleteChar(char *in, const char target) {
    char *t = strchr(in, target);
    if(t == NULL) {
        return -1;
    }
    int targetIndex = (int)(t - in); 
    memmove(&in[targetIndex], &in[targetIndex + 1], strlen(in) - targetIndex);
    return targetIndex;
}
