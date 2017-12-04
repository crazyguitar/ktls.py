import unittest
import hashlib
import time
import os

from threading import Thread

from .utils import client, server, set_ktls_sockopt

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def generate_test_file(name: str, size: int):
    """generate a random test file

    :param name: file name
    :param size: file size
    """
    with open(name, 'wb') as f:
        m = os.urandom(size)
        f.write(m)


def sendfile(outfd: int, infd: int, count: int):
    """doing sendfile

    :param outfd: outbound file descriptor 
    :param infd: inbound fd descriptor
    :param count: number of bytes writes to outbound
    """
    offset = 0
    st = os.fstat(infd)
    total = st.st_size
    byte = total

    while byte > 0:
        ret = os.sendfile(outfd, infd, offset, count)
        byte -= ret
        offset += ret


def send(client, infile, count: int):
    """doing send

    :param client: outbound ssl socket
    :param infile: inbound file object
    """
    fd = client.fileno()
    for c in iter(lambda: infile.read(count), b''):
        os.write(fd, c)


def recv(client, count: int) -> str:
    """doing ssl recv without zero-copy

    :param client: socket object of client
    :param count: number of bytes recv from socket buf

    :return: recv message
    """
    msg = b''
    for c in iter(lambda: client.recv(count), b''):
        msg += c

    return msg 


def read(infile, count: int) -> str:
    """doing ssl recv without zero-copy

    :param infile: file object of input file
    :param count: number of bytes read from file

    :return: read content
    """
    msg = b''
    for c in iter(lambda: infile.read(count), b''):
        msg += c

    return msg 


class TestKTLS(unittest.TestCase):

    TEST_FILE = os.path.join(CURRENT_DIR, ".ktls.tmp")
    HOST = 'localhost'
    PORT = 4433
    CERT = os.path.join(CURRENT_DIR, "cert.pem")
    KEY = os.path.join(CURRENT_DIR, "key.pem")
    CIPHER_SUITE = "ECDH-ECDSA-AES128-GCM-SHA256" 

    def setUp(self):
        """create test files"""
        generate_test_file(self.TEST_FILE, 4096)


    def tearDown(self):
        """remove test files"""
        if not os.path.exists(self.TEST_FILE):
            return
        os.unlink(self.TEST_FILE)

    def _client_thread(self, host, port):
        """ktls test client thread"""
        time.sleep(3)
        with open(self.TEST_FILE, 'rb') as f, \
             client(self.HOST, self.PORT) as c:
            msg = recv(c, 4096)
            raw = read(f, 4096)
            self.assertEqual(msg, raw)


    def test_send(self):
        """ktls send related test"""
        t = Thread(target=self._client_thread, args=(self.HOST, self.PORT,))
        t.daemon = True
        t.start()

        with open(self.TEST_FILE, 'rb') as f, \
             server(self.HOST, self.PORT, self.CERT, \
                    self.KEY, self.CIPHER_SUITE) as (s, sslctx):

            conn, addr = s.accept()
            sslconn = sslctx.wrap_socket(conn, server_side=True)
            sslconn = set_ktls_sockopt(sslconn)
            send(sslconn, f, 4096)
            sslconn.close()

        t.join()


    def test_sendfile(self):
        """ktls sendfile related test"""
        t = Thread(target=self._client_thread, args=(self.HOST, self.PORT,))
        t.daemon = True
        t.start()

        with open(self.TEST_FILE, 'rb') as f, \
             server(self.HOST, self.PORT, self.CERT, \
                    self.KEY, self.CIPHER_SUITE) as (s, sslctx):

            conn, addr = s.accept()
            sslconn = sslctx.wrap_socket(conn, server_side=True)
            sslconn = set_ktls_sockopt(sslconn)
            sendfile(sslconn.fileno(), f.fileno(), 4096)
            sslconn.close()

        t.join()
