#ifndef STRINGUTILS_H
#define STRINGUTILS_H

int * stringToIntArr(char * input, const char * delim, int * length);
char ** splitString(char * input, const char * delim, int * length);
int stringToInt(char * input);
int deleteChar(char *in, const char target);

#endif
