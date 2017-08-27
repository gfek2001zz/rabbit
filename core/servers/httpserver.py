#!/usr/bin/python

import sys
import logging
import socket
from wsgiref import simple_server

logger = logging.getLogger('rabbit.server')

def is_broken_pipe_error():
    exc_type, exc_value = sys.exc_info()[:2]
    return issubclass(exc_type, socket.error) and exc_value.args[0] == 32

class WSGIServer(simple_server.WSGIServer):
    def __init__(self, server_address, WSGIRequestHandler, ipv6=False):
        
        if ipv6:
            self.address_family = socket.AF_INET6
        super().__init__(server_address, WSGIRequestHandler);

    def handle_error(self, request, client_address):
        if is_broken_pipe_error():
            logger.info("- Broken pipe from %s\n", client_address)

        else:
            super().handle_error(request, client_address)

class ServerHandler(simple_server.ServerHandler):
    http_version = '1.1'

    def handler_error(self):
        if not is_broken_pipe_error():
            super().handle_error()

class WSGIRequestHandler(simple_server.WSGIRequestHandler):
    protocol_version = 'HTTP/1.1'

    def address_string(self):
        return self.client_address[0]

    def log_message(self, format, *args):
        extra = {
            'request': self.request,
            'server_time': self.log_date_time_string
        }

        if args[1][0] == '4':
            if args[0].startswith('\x16\x03'):
                extra['status_code'] = 500
                logger.error(
                    "You're accessing the development server over HTTPS, but "
                    "it only supports HTTP.\n", extra=extra,
                )
                return
            
        if args[1].isdigit() and len(args[1]) == 3:
            status_code = int(args[1])
            extra['status_code'] = status_code

            if status_code >= 500:
                level = logger.error
            elif status_code >= 400:
                level = logger.warning
            else:
                level = logger.info
        else:
            level = logger.info
        
        level(format, *args, extra=extra)\
    
    def get_environ(self):
        for k, v in self.headers.items():
            if '_' in k:
                del self.headers[k]
            
        return super().get_environ()

    def handle(self):
        self.close_connection = 1
        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def handle_one_request(self):
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request():
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self
        handler.run(self.server.get_app())

def run(addr, port, wsgi_handler, ipv6=False, server_cls=WSGIServer):
    server_address = (addr, port)

    httpd_cls = server_cls
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()