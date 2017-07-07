%module c_code
%{
#define SWIG_FILE_WITH_INIT
#include "c_code.h"
%}

int open_file(const char *name_file);
char *get_message();
void close_file();

