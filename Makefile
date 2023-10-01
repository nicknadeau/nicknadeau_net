CC = gcc
CFLAGS = -Wall
INCLUDE = -Isrc/native/include
BIN = src/native/nicknadeau

OBJ = \
	src/native/nicknadeau.o \
	src/native/about.o \
	src/native/blog.o \
	src/native/github.o \
	src/native/native.o \

%.o : %.c
	$(CC) $(INCLUDE) $(CFLAGS) -c -o $@ $<

all: src/native/nicknadeau

src/native/nicknadeau: $(OBJ)
	$(CC) $(INCLUDE) $(CFLAGS) -o $(BIN) $^

.PHONY: run
run: src/native/nicknadeau
	@printf "\nRunning site native version.\n\n"
	src/native/nicknadeau

.PHONY: clean
clean:
	rm -f $(BIN)
	rm -f $(OBJ)
