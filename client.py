#!/usr/bin/env python
import socket
import thread
import sys

class SnakeClient:

    RECV_BUFFER = 4096
    
    def recv_data(self):
        """ Receive data from other clients connected to server """
        while 1:
            try:
                self.recv_data = self.client_socket.recv(self.RECV_BUFFER)
            except:
                #Handle the case when server process terminates
                print "Server closed connection, thread exiting."
                thread.interrupt_main()
                break
            if not self.recv_data:
                # Recv with no data, server closed connection
                print "Server closed connection, thread exiting."
                thread.interrupt_main()
                break
            else:
                print "Received data: ", self.recv_data
    
    def send_command(self, command = ""):
        if command:
            self.client_socket.send(str(command))
        
    # def send_data(self):
    #     """Send data from other clients connected to server"""
    #     while 1:
    #         self.send_data = str(raw_input("Enter data to send (q or Q to quit):"))
    #         if self.send_data == "q" or self.send_data == "Q":
    #             self.client_socket.send(self.send_data)
    #             thread.interrupt_main()
    #             break
    #         else:
    #             self.client_socket.send(send_data)
    
    def __init__(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        thread.start_new_thread(self.recv_data,())
        thread.start_new_thread(self.send_command,())