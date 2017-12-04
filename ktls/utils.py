"""
From linux/include/uapi/linux/tls.h

#define TLS_CIPHER_AES_GCM_128                          51
#define TLS_CIPHER_AES_GCM_128_IV_SIZE                  8
#define TLS_CIPHER_AES_GCM_128_KEY_SIZE         16
#define TLS_CIPHER_AES_GCM_128_SALT_SIZE                4
#define TLS_CIPHER_AES_GCM_128_TAG_SIZE         16
#define TLS_CIPHER_AES_GCM_128_REC_SEQ_SIZE             8

#define TLS_SET_RECORD_TYPE	1

struct tls_crypto_info {
    __u16 version;
    __u16 cipher_type;
};

struct tls12_crypto_info_aes_gcm_128 {
    struct tls_crypto_info info;
    unsigned char iv[TLS_CIPHER_AES_GCM_128_IV_SIZE];
    unsigned char key[TLS_CIPHER_AES_GCM_128_KEY_SIZE];
    unsigned char salt[TLS_CIPHER_AES_GCM_128_SALT_SIZE];
    unsigned char rec_seq[TLS_CIPHER_AES_GCM_128_REC_SEQ_SIZE];
};
"""
import contextlib
import socket
import time
import json
import ssl
import os

from struct import pack


@contextlib.contextmanager
def server(host, port, certfile, keyfile, cipher_suite):
    """create a server context manager

    :param host: the server host
    :param port: the server port
    :param certfile: certificate file path
    :param keyfile: key file path
    :param cipher_suite: cipher suite (openssl format)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(10)
        sslctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslctx.load_cert_chain(certfile=certfile,
                               keyfile=keyfile)
        # set ssl ciphers
        sslctx.set_ciphers(cipher_suite)
        yield s, sslctx
    finally:
        s.close()


@contextlib.contextmanager
def client(host, port):
    """create a client context manager

    :param host: the server host
    :param port: the application port
    """
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sslctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslconn = sslctx.wrap_socket(c, server_hostname=host)
    try:
        sslconn.connect((host, port))
        yield sslconn
    finally:
        sslconn.close()


def set_ktls_sockopt(sslsock):
    """ set ktls related socket options (after handshake)

    :param sslsock: SSLSocket object
    """
    ktls_cipher = sslsock.ktls_cipher()
    if ktls_cipher is None:
        e_msg = "ktls only support ECDH-ECDSA-AES128-GCM-SHA256 now."
        raise OSError(e_msg)

    seq  = ktls_cipher['seq']
    key  = ktls_cipher['key']
    iv   = ktls_cipher['iv']
    salt = ktls_cipher['salt']

    tls12_crypto_info_aes_gcm_128 = pack(
         '2s2s8s16s4s8s',
         pack('=H', socket.TLS_1_2_VERSION),
         pack('=H', socket.TLS_CIPHER_AES_GCM_128),
         iv, key, salt, seq)

    # setsockopt ktl related options
    sslsock.setsockopt(socket.SOL_TCP,
                       socket.TCP_ULP, b'tls')

    sslsock.setsockopt(socket.SOL_TLS,
                       socket.TLS_TX,
                       tls12_crypto_info_aes_gcm_128)

    return sslsock
