CC = gcc
CFLAGS = -Wall
INCLUDE = -Isrc/native/include
BIN = src/native/nicknadeau
WEB = web_root website.tar.gz

OBJ = \
	src/native/nicknadeau.o \
	src/native/about.o \
	src/native/blog.o \
	src/native/github.o \
	src/native/native.o \

%.o : %.c
	$(CC) $(INCLUDE) $(CFLAGS) -c -o $@ $<

all: src/native/nicknadeau \
	pack \

src/native/nicknadeau: $(OBJ)
	$(CC) $(INCLUDE) $(CFLAGS) -o $(BIN) $^

.PHONY: run
run: src/native/nicknadeau
	@printf "\nRunning site native version.\n\n"
	src/native/nicknadeau

.PHONY: pack
pack:
	./pack.sh

.PHONY: clean
clean:
	rm -f $(BIN)
	rm -f $(OBJ)
	rm -rf $(WEB)
