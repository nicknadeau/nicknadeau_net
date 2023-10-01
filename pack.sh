#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
TARBALL=website.tar.gz
WEB_ROOT_NAME=web_root
WEB_ROOT="$SCRIPT_DIR"/"$WEB_ROOT_NAME"
HTML="$SCRIPT_DIR"/html
STYLES="$SCRIPT_DIR"/styles


function panicIfLastCommandFailed() {
	if [ $? -ne 0 ]; then
		echo "$1" >&2
		exit 1
	fi
}


if [ -z "$(ls "$HTML")" ]; then
	echo "WARNING: $HTML directory is empty so NOT packaging web assets since it would be an empty package!" >&2
	echo "Did you 'make clean' previously and blow away the contents?" >&2
	exit 1
fi

rm -rf "$WEB_ROOT" && \
	mkdir -p "$WEB_ROOT" && \
	cp -r "$HTML"/* "$WEB_ROOT" && \
	cp -r "$STYLES" "$WEB_ROOT" && \
	true
panicIfLastCommandFailed "Error: failed to package web assets!"

cd "$SCRIPT_DIR" && \
	rm -f "$TARBALL" && \
	tar -czvf "$TARBALL" "$WEB_ROOT_NAME" && \
	true
panicIfLastCommandFailed "Error: failed to create website tarball!"

echo "Successfully packaged web assets!"
echo "Raw assets are at: $WEB_ROOT"
echo "Assets tarball is at: $TARBALL"
