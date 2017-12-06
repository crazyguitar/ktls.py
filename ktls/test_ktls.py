import unittest
import time
import os

from threading import Thread

from .utils import (
    client,
    server,
    send,
    recv,
    read,
    sendfile,
    generate_test_file,
    set_ktls_sockopt)

from .config import (
    CONFIG_PWD,
    CONFIG_CERT,
    CONFIG_KEY,
    CONFIG_CIPHER_SUITE)

CURRENT_DIR = CONFIG_PWD


class TestKTLS(unittest.TestCase):

    TEST_FILE = os.path.join(CURRENT_DIR, ".ktls.tmp")
    HOST = 'localhost'
    PORT = 4433
    CERT = CONFIG_CERT
    KEY = CONFIG_KEY
    CIPHER_SUITE = CONFIG_CIPHER_SUITE

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
        time.sleep(1)
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
                server(self.HOST, self.PORT, self.CERT,
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
                server(self.HOST, self.PORT, self.CERT,
                       self.KEY, self.CIPHER_SUITE) as (s, sslctx):

            conn, addr = s.accept()
            sslconn = sslctx.wrap_socket(conn, server_side=True)
            sslconn = set_ktls_sockopt(sslconn)
            sendfile(sslconn.fileno(), f.fileno(), 4096)
            sslconn.close()

        t.join()

    def _client_echo_thread(self, host, port):
        """ktls test client thread"""
        time.sleep(1)
        with client(self.HOST, self.PORT) as c:
            smsg = b"Hello KTLS!"
            c.send(smsg)
            rmsg = recv(c, 1024)
            self.assertEqual(smsg, rmsg)

    def test_ktls_echo(self):
        host, port = self.HOST, self.PORT
        cert, key = self.CERT, self.KEY
        cipher = self.CIPHER_SUITE

        t = Thread(target=self._client_echo_thread, args=(host, port,))
        t.daemon = True
        t.start()

        with server(host, port, cert, key, cipher) as (s, ctx):
            conn, addr = s.accept()
            sslconn = ctx.wrap_socket(conn, server_side=True)
            sslconn = set_ktls_sockopt(sslconn)

            # echo
            fd = sslconn.fileno()
            rmsg = sslconn.recv(1024)
            os.write(fd, rmsg)

            # close the tls connection
            sslconn.close()

        t.join()
