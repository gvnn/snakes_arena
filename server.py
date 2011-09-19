#!/usr/bin/env python
import SocketServer
import os
import socket

conf = None #config obj

def get_available_ips():
    ips = []
    if os.name != "nt":
        try:
            import netifaces
            for i, interface in enumerate(netifaces.interfaces()):
                ifaddresses = netifaces.ifaddresses(str(interface))
                if netifaces.AF_INET in ifaddresses:
                    ips.append(ifaddresses[netifaces.AF_INET][0]["addr"])
        except ImportError, e:
            ips.append("127.0.0.1")
            ips.append(socket.gethostbyname(socket.gethostname()))
    else:
        # local and public network interface
        ips.append("127.0.0.1")
        ips.append(socket.gethostbyname(socket.gethostname()))
    return ips

class SnakeRequestHandler(SocketServer.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        conf.logger.debug('%s %s' % client_address)
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        socket = self.request[1]
        server._tmp_clients.append(socket)
        return

    def setup(self):
        conf.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        conf.logger.info("%s wrote: %s" % (self.client_address, data))
        return

    def finish(self):
        conf.logger.debug('finish')
        return SocketServer.BaseRequestHandler.finish(self)

class SnakeServer(SocketServer.TCPServer):
    
    _tmp_clients = []
    
    def __init__(self, server_address, handler_class=SnakeRequestHandler):
        conf.logger.debug('%s', server_address)
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        conf.logger.debug('server_activate')
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        conf.logger.debug('waiting for request')
        conf.logger.info('Handling requests')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        conf.logger.debug('handle_request')
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        conf.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        conf.logger.debug('process_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        conf.logger.debug('server_close')
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        conf.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        conf.logger.debug('close_request(%s)', request_address)
        return SocketServer.TCPServer.close_request(self, request_address)