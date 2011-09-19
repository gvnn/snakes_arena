#!/usr/bin/env python
import socket

conf = None #config obj

class SnakeClient:
    
    _sock = None
    _server_ip = ""
    _server_port = ""
    
    def __init__(self, ip, port):
        conf.logger.debug('client init')
        self._server_ip = ip
        self._server_port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self._sock.connect((self._server_ip, self._server_port))
        conf.logger.debug('client connect')
        self._sock.send("hissssss")
        while 1:
            data = self._sock.recv(1024)
            print data
            if data == 'Q':
                break;
    
    def send(self, msg):
        self._sock.send(msg)