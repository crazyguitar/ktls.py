#!/usr/bin/env python3.6

import types
import ssl
import os

from http.server import (
    HTTPServer,
    SimpleHTTPRequestHandler)

from ktls.utils import set_ktls_sockopt


def sendall(self, b):
    """ overwrite origin socket.sendall

    ref: cpython/Lib/socketserver.py +791
    """
    fd = self.fileno()
    os.write(fd, b)


class HTTPSServer(HTTPServer):

    def get_request(self):
        """ overwrite origin get_request for setting ktls

        ref: cpython/Lib/socketserver.py +490
        """
        conn, addr = super().get_request()

        # set ktls socket options
        conn = set_ktls_sockopt(conn)
        conn.sendall = types.MethodType(sendall, conn)
        return conn, addr


def run():

    host, port = "localhost", 4433
    cert, key = 'ktls/ca/cert.pem', 'ktls/ca/key.pem'
    handler = SimpleHTTPRequestHandler

    # prepare ssl context
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain(certfile=cert, keyfile=key)
    ctx.set_ciphers('ECDH-ECDSA-AES128-GCM-SHA256')

    # run the https server
    with HTTPSServer((host, port), handler) as httpd:
        httpd.socket = ctx.wrap_socket(httpd.socket,
                                       server_side=True)
        httpd.serve_forever()


try:
    run()
except KeyboardInterrupt:
    pass
