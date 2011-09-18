#!/usr/bin/env python
import SocketServer
import config

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "%s wrote:" % self.client_address[0]
        print data
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    config.load_config()
    HOST, PORT = config.config_values["server"]["host"], int(config.config_values["server"]["port"])
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()