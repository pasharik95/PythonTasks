#include "c_code.h"

int open_file(const char *name_file)
{
	f = fopen(name_file, "r");

	if (f == NULL) // if can not open file
	{
		return -1;
	}

	buff = malloc(SIZE_BUFF);

	return 0;
}

char *get_message()
{
	if (!feof(f))
		fgets(buff, SIZE_BUFF, f);
	else
		return NULL; // if file is finished

	return buff;
}

void close_file()
{
	fclose(f);

	free(buff);
}
