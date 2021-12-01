#include <stdio.h>
#include <stdlib.h>

#define INPUT_PATH "inputs/Day1.txt"

int main() {
    FILE *input;

    int depth = 0;
    int sz = 0;

    input = fopen(INPUT_PATH, "r");
    fseek(input, 0L, SEEK_END);
    sz = ftell(input);
    rewind(input);
    int *depths = (int *) malloc(sz * sizeof(int));
    int *windows = (int *) malloc((sz - 2) * sizeof(int));
    int window[3];

    int i = 0;
    fscanf(input, "%d", &depth);
    while (!feof(input)) {
        printf("%d\n", depth);

        if (i > 2) {
            window[0] = window[1];
            window[1] = window[2];
        }
        if(i < 2) {
            window[i] = depth;
        }
        else {
            window[2] = depth;
            windows[i - 2] = window[0] + window[1] + window[2];
        }
        depths[i] = depth;
        i++;
        fscanf(input, "%d", &depth);
    }
    fclose(input);

    int tally = 0;
    for (int i = 1; i < sz; i++) {
        if (depths[i - 1] < depths[i]) {
            tally++;
        }
    }

    printf("Increasing %d times\n", tally);

    tally = 0;
    for (int i = 1; i < sz - 2; i++) {
        if (windows[i - 1] < windows[i]) {
            tally++;
        }
    }

    printf("Windows increasing %d times\n", tally);
}
