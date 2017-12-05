# Playing Kernel TLS in Python

ktls.py provides several scripts to test linux kernel TLS in Python.

## Prerequest

1. Linux kernel 4.13 or above (option CONFIG\_TLS=y or CONFIG\_TLS=m)
2. openssl 1.0.x

## Install

#### Manual install cpython with supproting KTLS

```bash
$ git clone https://github.com/crazyguitar/cpython
$ cd cpython
$ ./configure --prefix=/usr --enable-optimizations
$ make -j 9 && sudo make altinstall
```

#### Using vagrant

```
$ vagrant init crazyguitar/xenial64 --box-version 20171205.0.0
$ vagrant up
$ vagrant ssh
```

## Run the tests

```
# run the lint
$ make lint

# run the tests
make test

# run all the tests and lint
$ make
```
