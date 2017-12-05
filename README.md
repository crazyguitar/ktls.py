# Playing with Kernel TLS in Python

[![Build Status](https://travis-ci.org/crazyguitar/ktls.py.svg?branch=master)](https://travis-ci.org/crazyguitar/ktls.py)

ktls.py provides several scripts to test linux kernel TLS in Python.

## Prerequisite

1. Linux kernel 4.13 or above (option CONFIG\_TLS=y or CONFIG\_TLS=m)
2. openssl 1.0.x

## Install

#### Manual install cpython with supproting KTLS

```bash
$ git clone -b v3.6.3-ktls-patch https://github.com/crazyguitar/cpython
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
# run lint
$ make lint

# run tests
$ make test

# run all tests and lint
$ make
```
