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

To generate all our HTML files from all our C files simply run:
```shell
make generate-html
```

Note that this command is additive-only. That is, it will update existing files or new files but if a native source file is being deleted it will not delete its generated file. If additive and deletive operations are desired it is best to clean out the generated files entirely first and trigger a mass re-generation (there are only a few source files so this doesn't take long):
```
make clean generate-html
```

## Packaging Website
To package the web frontend code up into a directory to be hosted out of, as well as a tarball, run:

```shell
make clean pack
```

## Putting It All Together
We can compile our C source, generate all of the corresponding HTML files from it, and then pack up our web contents by simply running:
```shell
make
```

Note that this command is additive-only (see the above section on auto-generating from native source) and if deletive operations are desired as well then use:
```shell
make clean all
```
