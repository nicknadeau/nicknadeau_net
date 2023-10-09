#include "nicknadeau.h"

#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <limits.h>
#include <errno.h>


LINK(about)
LINK(github)
LINK(native)


static void printInstructions() {
	printf(
		"To display a specific page, write the name of the page and then hit ENTER.\n"
		"To list the pages, write 'list' and then hit ENTER.\n"
		"To stop running, write 'exit' and then hit ENTER. Or, you know, the good ole CTRL+C.\n"
	);
}

static void list() {
	printf(
		"\nPages: 'about', 'native', 'github'"
		"\n"
	);
}

static bool stringEquals(const char *expected, const char *buffer, uint32_t bufferSize) {
	uint32_t expectedSize = strlen(expected);
	return (expectedSize == bufferSize) && (0 == strncmp(expected, buffer, expectedSize));
}

static void printPagePreamble(const char *pageName, uint32_t nameLength) {
	printf("\n===> Page: %.*s\n\n", nameLength, pageName);
}

int main(int argc, const char **argv)
{
	char buffer[BUFSIZ];
	printInstructions();
	printf("\n# ");
	fflush(stdout);
	int bytesRead = read(STDIN_FILENO, buffer, BUFSIZ);
	while (bytesRead > 0) {
		uint32_t bufferSize = bytesRead - 1;
		if (BUFSIZ == bytesRead) {
			fprintf(stderr, "...What exactly are you trying to do?\n");
			return 1;
		} else if (stringEquals("exit", buffer, bufferSize)) {
			return 0;
		} else if (stringEquals("list", buffer, bufferSize)) {
			list();
		} else if (stringEquals("about", buffer, bufferSize)) {
			printPagePreamble(buffer, bufferSize);
			about();
		} else if (stringEquals("native", buffer, bufferSize)) {
			printPagePreamble(buffer, bufferSize);
			native();
		} else if (stringEquals("github", buffer, bufferSize)) {
			printPagePreamble(buffer, bufferSize);
			github();
		} else {
			printInstructions();
		}
		printf("\n# ");
		fflush(stdout);
		bytesRead = read(STDIN_FILENO, buffer, BUFSIZ);
	}
	if (0 == bytesRead) {
		fprintf(stderr, "**Exiting -> stdin was closed!\n");
	} else {
		fprintf(stderr, "**Exiting -> error reading stdin! errno=%d\n", errno);
	}
	return 1;
}
