CC = gcc
CFLAGS = -Wall
INCLUDE = -Isrc/native/include
BIN = src/native/nicknadeau
WEB = html web_root website.tar.gz


OBJ = \
	src/native/nicknadeau.o \
	src/native/about.o \
	src/native/github.o \
	src/native/native.o \

%.o : %.c
	$(CC) $(INCLUDE) $(CFLAGS) -c -o $@ $<

all: src/native/nicknadeau \
	generate-html \
	pack \

src/native/nicknadeau: $(OBJ)
	$(CC) $(INCLUDE) $(CFLAGS) -o $(BIN) $^

.PHONY: run
run: src/native/nicknadeau
	@printf "\nRunning site native version.\n\n"
	src/native/nicknadeau

.PHONY: generate-html
generate-html:
	python3 generate/all_html_from_native.py ./src/native ./html

.PHONY: pack
pack:
	./pack.sh

.PHONY: clean
clean:
	rm -f $(BIN)
	rm -f $(OBJ)
	rm -rf $(WEB)
