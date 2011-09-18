#!/usr/bin/env python
import socket

conf = None #config obj

class SnakeClient:
    
    _sock = None
    _server_ip = ""
    _server_port = ""
    
    def __init__(self, ip, port):
        conf.logger.debug('SnakeClient __init__')
        self._server_ip = ip
        self._server_port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        """docstring for connect"""
        self._sock.connect((self._server_ip, self._server_port))
        self._sock.send("hissssss")