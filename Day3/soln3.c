#include <stdlib.h>
#include <string.h>
#include "fileUtils.h"
#include <math.h>

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

char * mostCommon(char **list, int length, int width) {
    int *sum = (int *) malloc(width * sizeof(int));
    char *common = (char *) malloc(width * sizeof(char));

    for(int w = 0; w < width; w++) {
        sum[w] = 0;
        for(int i = 0; i < length; i++) {
            if(list[i][w] == '1') {
                sum[w] += 1;
            }
        }
        if (sum[w] * 2 > length) {
            common[w] = '1';
        }
        else {
            common[w] = '0';
        }
    }

    return common;
}

int main() {
    int length;
    char ** lines = getInputLines(3, &length);

    printf("%s\n", mostCommon(lines, length, 12));
    
    printf("%d\n", binToDec(mostCommon(lines, length, 12)));
/*    int totalLines = 1000;
    FILE *input = getInput(3);
    if (input == NULL) {
        exit(EXIT_FAILURE);
    }

    char **all = malloc(totalLines * sizeof(char *));

    ssize_t read;
    char * line = NULL;
    size_t len = 0;

    read = getline(&line, &len, input);
    line[strlen(line) - 1] = '\0';
    int strLength = strlen(line);

    for(int i = 0; i < totalLines; i++) {
        all[i] = malloc(strLength * sizeof(char));
    }
    all[0] = line;

    int index = 1;
    while ((read = getline(&line, &len, input)) != -1) {
        line[strlen(line) - 1] = '\0';
        all[index] = line;
    }

  */  
}
