#!/usr/bin/env python
import socket
import thread
import sys

class SnakeClient:

    RECV_BUFFER = 4096
    
    _confobj = None #: config object
    
    def recv_data(self):
        """ Receive data from other clients connected to server """
        while 1:
            try:
                self.recv_data = self.client_socket.recv(self.RECV_BUFFER)
            except:
                #Handle the case when server process terminates
                self._confobj.logger.debug("Server closed connection, thread exiting.")
                thread.interrupt_main()
                break
            if not self.recv_data:
                # Recv with no data, server closed connection
                self._confobj.logger.debug("Server closed connection, thread exiting.")
                thread.interrupt_main()
                break
            else:
                self._confobj.logger.debug("Received data: %s" % self.recv_data)
    
    def send_command(self, command = ""):
        if command:
            self.client_socket.send(str(command))
            if command == "q":
                sys.exit()
    
    def __init__(self, ip, port, conf):
        self._confobj = conf
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        thread.start_new_thread(self.recv_data,())
        thread.start_new_thread(self.send_command,())