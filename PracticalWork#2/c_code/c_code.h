/*c_code.h*/

#ifndef CODE_H
#define CODE_H

#include <stdlib.h>
#include <stdio.h>

#define SIZE_BUFF 1024 // max size of line
FILE *f; // file
char *buff; // buffer for one line

int open_file(const char *name_file);
char *get_message();
void close_file();

#endif
