#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stringUtils.h"

int stringToInt(char * input) {
    char *end;
    return strtol(input, &end, 10);
}

int * stringToIntArr(char * input, const char * delim, int * length) {
    char * token;
    size_t size = 0;

    char *counter = NULL;
    counter = strdup(input); 
    token = strtok(counter, delim);

    while (token != NULL) {
        size++;
        token = strtok(NULL, delim);
    }

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
