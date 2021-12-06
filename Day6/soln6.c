#include <stdio.h>
#include "fileUtils.h"
#include <string.h>
#include <stdlib.h>

#define MAX_FISH_PD 8
#define AVG_FISH_PD 6

double propogateTo(double fish[], int days) {
    for (int i = fish[MAX_FISH_PD + 1]; i < days; i++) {
        double splitters = fish[0];

        for (int i = 0; i < MAX_FISH_PD; i++) {
            fish[i] = fish[i + 1];
        }
        fish[MAX_FISH_PD] = splitters;
        fish[AVG_FISH_PD] += splitters;
    }

    fish[MAX_FISH_PD + 1] = days;

    double total = 0;
    for (int i = 0; i < MAX_FISH_PD + 1; i++) {
        total += fish[i];
    }

    return total;
}

int main() {
    FILE *input = getInput(6);
    if (input == NULL) {
        exit(EXIT_FAILURE);
    }

    ssize_t read;
    char * line = NULL;
    size_t len = 0;

    read = getline(&line, &len, input);
    
    int length = strlen(line) / 2;

    double *fish = (double *) malloc((MAX_FISH_PD + 2) * sizeof(double));

    for (int i = 0; i < MAX_FISH_PD + 2; i++) {
        fish[i] = 0;
    }

    char *pt;
    pt = strtok (line,",");
    while (pt != NULL) {
        int a = atoi(pt);
        fish[a]++;
        pt = strtok (NULL, ",");
    }

    printf("First: %.0f\n", propogateTo(fish, 80));
    printf("Second: %.0f\n", propogateTo(fish, 256));
}
