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
# insert tls kernel module if tls is built as module
$ sudo modprobe tls

# checking tls kernel module has been inserted
$ $ lsmod | grep tls
tls                    20480  0

# run lint
$ make lint

# run tests
$ make test

# run all tests and lint
$ make
```

## Reference

1. [KTLS: Linux Kernel Transport Layer Security](https://netdevconf.org/1.2/papers/ktls.pdf)
2. [brno university of technology linux vpn performance and optimization](https://dspace.vutbr.cz/bitstream/handle/11012/61908/18032.pdf?sequence=2&isAllowed=y)
3. [Improving High-Bandwidth TLS in the FreeBSD kernel](https://openconnect.netflix.com/publications/asiabsd_tls_improved.pdf)
4. [Optimizing TLS for High-Bandwidth Applications in FreeBSD](https://people.freebsd.org/~rrs/asiabsd_2015_tls.pdf)
5. [TLS in the kernel](https://lwn.net/Articles/666509/)
6. [Playing with kernel TLS in Linux 4.13 and Go](https://blog.filippo.io/playing-with-kernel-tls-in-linux-4-13-and-go/)
