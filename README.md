# nicknadeau.net

The source code backing [nicknadeau.net](https://nicknadeau.net).

The pages of my website display my page content structured inside C code syntax. This is real runnable C. As such, it only makes sense you should be able to compile and execute the "site" on the commandline.

The "native" portion of the site refers to all of the C source code, from which the real web frontend is auto-generated.

## Building And Running Natively
To build the site-as-commandline binary:

```shell
make clean src/native/nicknadeau
```

To run the site-as-commandline binary, either execute the binary directly or:

```shell
make clean run
```

## Auto-generating HTML From Native Source
The site is defined as a collection of compilable C source files that can be run on the commandline. It would just be wasteful and error-prone to rewrite them as HTML for the web too. Instead, we just auto-generate the HTML from the C files.

To generate an HTML file from a C file simply run:
```shell
python3 generate/html_from_native.py <source-path>
```

Example:
```shell
python3 generate/html_from_native.py src/native/about.c
```

## Packaging Website
To package the web frontend code up into a directory to be hosted out of, as well as a tarball, run:

```shell
make clean pack
```
