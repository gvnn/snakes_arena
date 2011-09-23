#!/usr/bin/env python
import socket
import thread
import sys
import pyglet

class SnakeClient(pyglet.event.EventDispatcher):

    RECV_BUFFER = 4096
    
    confobj = None #: config object
    
    def recv_data(self):
        """ Receive data from other clients connected to server """
        while 1:
            try:
                self.recv_data = self.client_socket.recv(self.RECV_BUFFER)
            except:
                #Handle the case when server process terminates
                self.confobj.logger.debug("Server closed connection, thread exiting.")
                thread.interrupt_main()
                break
            if not self.recv_data:
                # Recv with no data, server closed connection
                self.confobj.logger.debug("Server closed connection, thread exiting.")
                thread.interrupt_main()
                break
            else:
                self.parse_data(self.recv_data)
    
    def parse_data(self, data):
        if data:
            self.confobj.logger.debug("%s" % data)
            args = ("%s" % data).split(":")
            if len(args) == 3:
                clientid = ("%s:%s" % (args[0], args[1]))
                options = {
                    'new' : lambda c: self.dispatch_remote_connected(c),
                    'up' : lambda c: self.dispatch_remote_change_direction(c, 'up'),
                    'left' : lambda c: self.dispatch_remote_change_direction(c, 'left'),
                    'right' : lambda c: self.dispatch_remote_change_direction(c, 'right'),
                    'down' : lambda c: self.dispatch_remote_change_direction(c, 'down'),
                    'quit' : lambda c: self.dispatch_remote_disconnected(c)
                }[str(args[2])](clientid)
    
    def dispatch_remote_connected(self, clientid):
        self.dispatch_event("on_remote_connected", clientid)
        
    def dispatch_remote_disconnected(self, clientid):
        self.dispatch_event("on_remote_disconnected", clientid)
        
    def dispatch_remote_change_direction(self, clientid, direction):
        self.dispatch_event("on_remote_change_direction", clientid, direction)
    
    def send_command(self, command = ""):
        if command:
            self.client_socket.send(str(command))
            if command == "q":
                sys.exit()
    
    def __init__(self, ip, port, conf):
        self.confobj = conf
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        thread.start_new_thread(self.recv_data,())
        thread.start_new_thread(self.send_command,())

SnakeClient.register_event_type('on_remote_connected')
SnakeClient.register_event_type('on_remote_change_direction')
SnakeClient.register_event_type('on_remote_disconnected')