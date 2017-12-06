import unittest
import types
import time
import ssl
import os

from threading import Thread
from http import server, client

from .utils import set_ktls_sockopt
from .config import (
    CONFIG_PWD,
    CONFIG_CERT,
    CONFIG_KEY,
    CONFIG_CLIENT_CERT,
    CONFIG_CLIENT_KEY,
    CONFIG_CIPHER_SUITE)


CURRENT_DIR = CONFIG_PWD

HTML = b"""
<html>
    <head></head>
    <body><h1>Hello KTLS</h1></body>
</html>
"""


def write(self, b):
    sock = set_ktls_sockopt(self._sock)
    fd = sock.fileno()
    return os.write(fd, b)


class HTTPSServer(server.HTTPServer):

    def __init__(self, server_address, handler_class, context):
        super().__init__(server_address, handler_class)
        self.context = context

    def get_request(self):
        conn, addr = super().get_request()
        sslconn = self.context.wrap_socket(conn, server_side=True)
        return sslconn, addr


class KTLShttpsHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write = types.MethodType(write, self.wfile)
        self.wfile.write(HTML)

    def log_request(self, code=None, size=None):
        return


class TestKTLShttps(unittest.TestCase):

    HOST = 'localhost'
    PORT = 4433
    CERT = CONFIG_CERT
    KEY = CONFIG_KEY
    CIPHER_SUITE = CONFIG_CIPHER_SUITE

    CLIENT_CERT = CONFIG_CLIENT_CERT
    CLIENT_KEY = CONFIG_CLIENT_KEY

    def _server_thread(self, httpd):
        """start a https server thread"""
        httpd.serve_forever()

    def test_https(self):
        """run the ktls-https test"""
        certfile, keyfile = self.CERT, self.KEY
        sslctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
        sslctx.set_ciphers(self.CIPHER_SUITE)

        host, port = self.HOST, self.PORT

        with HTTPSServer((host, port), KTLShttpsHandler, sslctx) as httpd:

            t = Thread(target=self._server_thread, args=(httpd,))
            t.daemin = True
            t.start()

            time.sleep(1)
            sslctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslctx.load_verify_locations(self.CERT)
            sslctx.load_cert_chain(self.CLIENT_CERT, self.CLIENT_KEY)

            conn = client.HTTPSConnection(host, port, context=sslctx)
            conn.request('GET', '/')
            resp = conn.getresponse()

            # check response
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.reason, 'OK')
            self.assertEqual(resp.read(), HTML)

            # shutdown http server
            httpd.shutdown()
