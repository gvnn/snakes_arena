#!/usr/bin/env python
import os
import socket
import select
import string

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
    
class SnakeServer():
    
    _confobj = None #: config object
    
    _server_ip = ""
    
    _server_port = 0
    
    _server_socket = None
    
    CONNECTION_LIST = [] #: List to keep track of socket descriptors
    
    def __init__(self, ip, port, conf):
        self._confobj = conf
        self._server_ip = ip
        self._server_port = port

    def broadcast_data(self, sock, message):
        """Send broadcast message to all clients other than the
        server socket and the client socket from which the data is received."""
        for socket in self.CONNECTION_LIST:
            if socket != self._server_socket and socket != sock:
                socket.send("%s" % message)
            
    def start(self):
        RECV_BUFFER = 4096
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._server_ip, self._server_port))
        self._server_socket.listen(10)
        self.CONNECTION_LIST.append(self._server_socket)
        self._confobj.logger.debug("TCP/IP Chat server process started");
        while 1:
            # get the list sockets
            read_sockets,write_sockets,error_sockets = select.select(self.CONNECTION_LIST,[],[])
            for sock in read_sockets:
                if sock == self._server_socket:
                    #new connection
                    sockfd, addr = self._server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)
                    self._confobj.logger.debug("client (%s, %s) connected" % addr)
                    #broadcast to other arenas the new client
                    self.broadcast_data(sockfd, "%s:%s:new" % addr)
                else:
                    # Data recieved
                    try:
                        data = sock.recv(RECV_BUFFER)
                    except:
                        self.broadcast_data(sock, "%s:%s:quit" % addr)
                        self._confobj.logger.debug("client (%s, %s) is offline" % addr)
                        sock.close()
                        self.CONNECTION_LIST.remove(sock)
                        continue
                    if data:
                        # The client sends some valid data, process it
                        if data == "q" or data == "Q":
                            self.broadcast_data(sock, "%s:%s:quit" % addr)
                            self._confobj.logger.debug("client (%s, %s) quits" % addr)
                            sock.close()
                            self.CONNECTION_LIST.remove(sock)
                        else:
                            self.broadcast_data(sock, data)
        self._server_socket.close()