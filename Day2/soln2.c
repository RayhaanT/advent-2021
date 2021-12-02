#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INPUT_PATH "inputs/Day2.txt"

int main() {
    FILE *input;

    int depth = 0;
    int aim = 0;
    int horizontal = 0;

    input = fopen(INPUT_PATH, "r");

    int x = 0;
    char command[10]; // largest word is `forward`
    fscanf(input, "%s %d", command, &x);
    while(!feof(input)) {
        if(strcmp(command, "forward") == 0) {
            horizontal += x;
            depth += aim * x;
        }
        else if(strcmp(command, "up") == 0) {
            aim -= x;
        }
        else if(strcmp(command, "down") == 0) {
            aim += x;
        }
        else {
            perror("Error: no match");
            return 1;
        }
        fscanf(input, "%s %d", command, &x);
    }

    printf("First: %d\n", aim * horizontal);
    printf("Second: %d\n", depth * horizontal);
}
