#include <stdio.h>
#include <stdlib.h>
#include "stringUtils.h"
#include "fileUtils.h"
#include "stdbool.h"
#include <string.h>
#include <math.h>

#define ALL_CHARS "abcdefg"

bool match(const char * map, const char * src) {
    size_t length = strlen(map);
    for(int i = 0; i < length; i++) {
        if(strchr(src, map[i]) == NULL) {
            return false;
        }
    }
    return true;
}

bool exactMatch(const char *a, const char *b) {
    return match(a, b) && match(b, a);
}

char * inverse(char *code) {
    char * everything = strdup(ALL_CHARS);
    size_t length = strlen(code);
    
    for(int i = 0; i < length; i++) {
        deleteChar(everything, code[i]);
    }

    return everything;
}

char * common(char ** codes, size_t length) {
    char * everything = strdup(ALL_CHARS);
    ssize_t eLen = strlen(everything);
    int deleted = 0;

    for(int l = 0; l < eLen; l++) {
        for(int i = 0; i < length; i++) {
            if(strchr(codes[i], everything[l - deleted]) == NULL) {
                int ind = deleteChar(everything, everything[l - deleted]);
                if(ind > -1) {
                    deleted++;
                }
            }
        }
    }

    return everything;
}

char ** decode(char ** codes, size_t size) {
    char ** map = malloc(10 * sizeof(char *));

    for(int i = 0; i < size; i++) {
        ssize_t len = strlen(codes[i]);
        switch(len) {
            case 2:
                map[1] = codes[i];
                break;
            case 3:
                map[7] = codes[i];
                break;
            case 4:
                map[4] = codes[i];
                break;
            case 7:
                map[8] = codes[i];
                break;
            default:
                break;
        }
    }

    for(int i = 0; i < size; i++) {
        ssize_t len = strlen(codes[i]);
        char * c = codes[i];
        switch(len) {
            case 5:
                if(match(map[1], c))
                    map[3] = c;
                if(match(inverse(map[4]), c))
                    map[2] = c;
                break;
            case 6:
                if(!match(map[1], c))
                    map[6] = c;
                if(!match(inverse(map[4]), c))
                    map[9] = c;
                break;
            default:
                break;
        }
    }

    char *commonSet[5] = {
            map[2],
            map[3],
            map[4],
            map[6],
            map[9]
            };

    char * zeroDelim = common(commonSet, 5);
    map[0] = inverse(zeroDelim);

    for(int i = 0; i < size; i++) {
        if(strlen(codes[i]) == 5 && match(inverse(map[2]), codes[i])) {
            map[5] = codes[i];
            break;
        }
    }

    return map;
}

int main() {
    int fileLength;
    char ** lines = getInputLines(8, &fileLength);

    long firstTotal = 0;
    long secondTotal = 0;

    for(int i = 0; i < fileLength; i++) {
        int inputLength;
        int outputLength;
        char ** blocks = splitString(lines[i], "|", &inputLength);
        char ** inputs = splitString(blocks[0], " ", &inputLength);
        char ** outputs = splitString(blocks[1], " ", &outputLength);

        char ** map = decode(inputs, inputLength);
        int displayOut = 0;

        for(int o = 0; o < outputLength; o++) {
            for(int x = 0; x < 10; x++) {
                if(exactMatch(outputs[o], map[x])) {
                    displayOut += x*pow(10, 3-o);
                    if(x == 1 || x == 4 || x == 7 || x == 8) {
                        firstTotal++;
                    }
                    break;
                }
            }
        }
        secondTotal+=displayOut;
        displayOut=0;
    }

    printf("First: %d\n", firstTotal);
    printf("Second: %d\n", secondTotal);
}
