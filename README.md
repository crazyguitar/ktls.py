# Playing with Kernel TLS in Python

[![Build Status](https://travis-ci.org/crazyguitar/ktls.py.svg?branch=master)](https://travis-ci.org/crazyguitar/ktls.py)

ktls.py provides serveral tests and scripts to play linux kernel TLS in [cpython](https://github.com/crazyguitar/cpython/commit/3f11d3e046e4ad8630e15feaf6cd848d1f73a324). 
The idea was inspired from [PLAYING WITH KERNEL TLS IN LINUX 4.13 AND GO](https://blog.filippo.io/playing-with-kernel-tls-in-linux-4-13-and-go/).

## Prerequisite

1. Linux kernel 4.13 or above (option CONFIG\_TLS=y or CONFIG\_TLS=m)
2. openssl 1.0.x
3. The ktls patch of [cpython](https://github.com/crazyguitar/cpython/tree/v3.6.3-ktls-patch)

## Install

#### Manual install cpython with supproting KTLS

```bash
$ git clone -b v3.6.3-ktls-patch https://github.com/crazyguitar/cpython
$ cd cpython
$ ./configure --prefix=/usr --enable-optimizations
$ make -j 9 && sudo make altinstall
$ git clone https://github.com/crazyguitar/ktls.py.git
$ cd ktls.py
$ python3.6 https.py &
$ wget -qO- https://localhost:4433 --no-check-certificate
```

#### Using vagrant

```
$ vagrant init crazyguitar/xenial64 --box-version 20171205.0.0
$ vagrant up
$ vagrant ssh
vagrant@vagrant:~$ git clone https://github.com/crazyguitar/ktls.py.git
vagrant@vagrant:~$ cd ktls.py
vagrant@vagrant:~/ktls.py$ python3.6 https.py &
[2] 7866
vagrant@vagrant:~/ktls.py$ wget -qO- https://localhost:4433 --no-check-certificate 
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
