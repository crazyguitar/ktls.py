import unittest
import time
import os

from multiprocessing import Process

from .utils import (
    client,
    server,
    recv,
    read,
    generate_test_file)

from .config import (
    CONFIG_PWD,
    CONFIG_CERT,
    CONFIG_KEY,
    CONFIG_CIPHER_SUITE)

CURRENT_DIR = CONFIG_PWD


class TestTLSSend(unittest.TestCase):

    TEST_FILE = os.path.join(CURRENT_DIR, ".sendfile.tmp")
    HOST = 'localhost'
    PORT = 4433
    CERT = CONFIG_CERT
    KEY = CONFIG_KEY
    CIPHER_SUITE = CONFIG_CIPHER_SUITE
    BS = 4096

    def _server_process(self, host, port, cert, key, cipher):
        tmp_file = self.TEST_FILE

        print()  # just print a newline

        for flen in range(512, 1024, 64):
            generate_test_file(tmp_file, self.BS * flen)

            with open(tmp_file, 'rb') as f, \
                    server(host, port, cert, key, cipher) as (s, ctx):

                conn, addr = s.accept()
                sslconn = ctx.wrap_socket(conn, server_side=True)

                s = time.time()
                for c in iter(lambda: f.read(8192), b''):
                    sslconn.send(c)
                cost = time.time() - s

                print(f'send cost: {cost} (file size: {self.BS * flen})')

                sslconn.close()

            if os.path.exists(tmp_file):
                os.unlink(tmp_file)

    def _client_process(self, host, port):
        for _ in range(512, 1024, 64):
            time.sleep(1)
            tmp_file = self.TEST_FILE
            with open(tmp_file, 'rb') as f, \
                    client(self.HOST, self.PORT) as c:
                msg = recv(c, 8192)
                raw = read(f, 8192)
                self.assertEqual(msg, raw)

    def test_diff_sieze_performance(self):
        """test sendfile performance with different file size"""
        host, port = self.HOST, self.PORT
        cert, key = self.CERT, self.KEY
        cipher = self.CIPHER_SUITE

        p = Process(target=self._client_process, args=(host, port,))
        p.daemon = True
        p.start()

        self._server_process(host, port, cert, key, cipher)

        p.join()
