#include "nicknadeau.h"

#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <limits.h>
#include <errno.h>


LINK(about)
LINK(blog)
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
		"\nPages: 'about', 'native', 'github', 'blog [post id]'"
		"\n\nNote: the 'post id' of a blog post is the number in square brackets listed on the blog page."
		"\nTo view the blog page itself and not a specific post, omit the post id."
		"\n"
	);
}

static bool stringEquals(const char *expected, const char *buffer, uint32_t bufferSize) {
	uint32_t expectedSize = strlen(expected);
	return (expectedSize == bufferSize) && (0 == strncmp(expected, buffer, expectedSize));
}

static bool stringBeginsWith(const char *prefix, const char *buffer, uint32_t bufferSize) {
	uint32_t prefixSize = strlen(prefix);
	return (prefixSize <= bufferSize) && (0 == strncmp(prefix, buffer, prefixSize));
}

static uint32_t getBlogPostId(const char *buffer, uint32_t bufferSize, bool *out_hasId, bool *out_isInvalidId) {
	bool hasId = false;
	uint32_t prefixSize = strlen("blog");
	uint32_t id;
	if (prefixSize < bufferSize) {
		long value = strtol(buffer + prefixSize, NULL, 10);
		if ((LONG_MIN == value) || (LONG_MAX == value)) {
			*out_isInvalidId = true;
			return 0;
		}
		id = (uint32_t) value;
		hasId = true;
	}
	*out_hasId = hasId;
	return id;
}

static void displayBlogPost(uint32_t postId) {
	printf("Displaying post %u\n", postId);
	//TODO implement for real.
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
		} else if (stringBeginsWith("blog", buffer, bufferSize)) {
			bool hasId = false;
			bool isInvalidId = false;
			uint32_t postId = getBlogPostId(buffer, bufferSize, &hasId, &isInvalidId);
			if (isInvalidId) {
				fprintf(stderr, "Invalid 'post id' given. Must be an integer.\n");
			} else if (hasId) {
				displayBlogPost(postId);
			} else {
				printPagePreamble(buffer, bufferSize);
				blog();
			}
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
