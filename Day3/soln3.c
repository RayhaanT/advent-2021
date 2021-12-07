#include <stdlib.h>
#include <string.h>
#include "fileUtils.h"
#include <math.h>
#include <stdbool.h>

unsigned int binToDec(char *bin) {
    double total = 0;
    int length = strlen(bin);
    
    for(int i = 0; i < length; i++) {
        if(bin[i] == '1') {
            total += pow(2, length - i - 1);
        }
    }
    
    return (unsigned int)total;
}

int mostCommonDigit(int *list, int length, int index, bool favourHigh) {
    int map = pow(2, index);
    int sum = 0;
    int effectiveLength = length;
    for(int i = 0; i < length; i++) {
        if(list[i] < 0) {
            effectiveLength--;
            continue;
        }
        if(list[i] & map) {
            sum++;
        }
    }

    int common = sum * 2 > effectiveLength ? map : 0;
    if(favourHigh && sum * 2 == effectiveLength) {
        common = map;
    }

    return common;
}

int mostCommon(int *list, int length, int width) {
    int common = 0;
    for(int i = 0; i < width; i++) {
        common += mostCommonDigit(list, length, i, false);
    }

    return common;
}

int getReading(int *codes, int length) {
    int survivor = -1;
    for(int i = 0; i < length; i++) {
        if(codes[i] != -1) {
            if (survivor != -1) {
                return -1;
            }
            survivor = codes[i];
            continue;
        }
    }
    return survivor;
}

int main() {
    int length;
    char ** lines = getInputLines(3, &length);
    int *codes = (int *) malloc(length * sizeof(int));
    int width = strlen(lines[0]);

    for(int i = 0; i < length; i++) {
        codes[i] = binToDec(lines[i]);
    }

    int common = mostCommon(codes, length, width);
    int first = common * (pow(2, width) - 1 - common);
    printf("First: %d\n", first);

    int *storeCodes = malloc(length * sizeof(int));
    memcpy(storeCodes, codes, length * sizeof(int));

    int reading;
    int index = 0;

    while((reading = getReading(codes, length)) == -1 && index < width) {
        int target = mostCommonDigit(codes, length, width - index - 1, true);
        int map = pow(2, width - index - 1);
        for(int i = 0; i < length; i++) {
            if(codes[i] < 0) {
                continue;
            }
            if((codes[i] & map) != target) {
                codes[i] = -1;
            }
        }
        index++;
    }
    int oxygen = reading;

    index = 0;

    // This is almost the same as the first but I was too lazy to abstract it
    memcpy(codes, storeCodes, length * sizeof(int));
    while((reading = getReading(codes, length)) == -1 && index < width) {
        int target = mostCommonDigit(codes, length, width - index - 1, true);
        int map = pow(2, width - index - 1);
        for(int i = 0; i < length; i++) {
            if(codes[i] < 0) {
                continue;
            }
            if((codes[i] & map) == target) {
                codes[i] = -1;
            } else {
            }
        }
        index++;
    }
    int co2 = reading;

    printf("Second: %d\n", oxygen * co2);

    return 0;
}
