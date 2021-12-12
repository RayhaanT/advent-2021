#ifndef FILEUTILS_H
#define FILEUTILS_H

#include <stdio.h>

FILE * getInput(int day);
int getFileSize(int day);
char ** getInputLines(int day, int *length);
int intComparator (const void * aP, const void * bP);
int longComparator (const void * aP, const void * bP);
int stringComparator (const void* a, const void* b);

#endif
