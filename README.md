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
