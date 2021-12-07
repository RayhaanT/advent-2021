#include <stdio.h>
#include <stdlib.h>
#include "fileUtils.h"
#include "stringUtils.h"

int comparator (const void * aP, const void * bP) {
    int a = *((int*)aP);
    int b = *((int*)bP);
    if (a > b) return  1;
    if (b < a) return -1;
    return 0;
}

float median(int list[], int length) {
    qsort(list, length, sizeof(int), comparator);

    double medianIndex = length/2;
    int truncated = (int)medianIndex;
    if(medianIndex == truncated) {
        return list[truncated];
    }
    else {
        return (list[truncated] + list[truncated + 1])/2;
    }
}

float mean(const int list[], int length) {
    long total = 0;
    for(int i = 0; i < length; i++) {
        total += list[i];
    }

    return total/length;
}

int sumTo(const int n) {
    return (n*(n + 1))/2;
}

int min(const int a, const int b) {
    return a < b ? a : b;
}

int main() {
    int length;
    char ** lines = getInputLines(7, &length);
    int *positions = stringToIntArr(lines[0], ",", &length);

    int med = (int)median(positions, length);
    int lowMean = (int)mean(positions, length);
    int highMean = lowMean + 1;
    
    int firstTotal = 0;
    int lowTotal = 0;
    int highTotal = 0;
    for (int i = 0; i < length; i++) {
        int pos = positions[i];
        firstTotal += abs(med - pos);
        highTotal += sumTo(abs(highMean - pos));
        lowTotal += sumTo(abs(lowMean - pos));
    }

    printf("First: %d\n", firstTotal);
    printf("Second: %d\n", min(highTotal, lowTotal));
}
