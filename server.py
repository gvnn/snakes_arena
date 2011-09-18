#!/usr/bin/env python
import SocketServer

conf = None #config obj

class SnakeRequestHandler(SocketServer.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        conf.logger.debug('%s %s' % client_address)
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
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

class SnakeServer(SocketServer.UDPServer):
    
    def __init__(self, server_address, handler_class=SnakeRequestHandler):
        conf.logger.debug('%s', server_address)
        SocketServer.UDPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        conf.logger.debug('server_activate')
        SocketServer.UDPServer.server_activate(self)
        return

    def serve_forever(self):
        conf.logger.debug('waiting for request')
        conf.logger.info('Handling requests')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        conf.logger.debug('handle_request')
        return SocketServer.UDPServer.handle_request(self)

    def verify_request(self, request, client_address):
        conf.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.UDPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        conf.logger.debug('process_request(%s, %s)', request, client_address)
        return SocketServer.UDPServer.process_request(self, request, client_address)

    def server_close(self):
        conf.logger.debug('server_close')
        return SocketServer.UDPServer.server_close(self)

    def finish_request(self, request, client_address):
        conf.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.UDPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        conf.logger.debug('close_request(%s)', request_address)
        return SocketServer.UDPServer.close_request(self, request_address)