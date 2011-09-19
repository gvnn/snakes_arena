#!/usr/bin/env python
import cocos
import pyglet

class Arena(cocos.layer.Layer):
    
    is_event_handler = True     #: enable pyglet's events
    
    _reptiles = [] #array of clients
    
    _tmp_socket = None
    
    _tmp_server_socket = None
    
    keys_pressed = None
    
    def __init__(self):
        super(Arena, self).__init__()
        self.keys_pressed = set()
    
    def on_key_press (self, key, modifiers):
        self.keys_pressed.add(key)
        self.send_key()
    
    def on_key_release (self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
    
    def send_key(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: '+','.join(key_names)
        if self._tmp_socket:
            self._tmp_socket.send(text)
        if self._tmp_server_socket:
            for socket in self._tmp_server_socket._tmp_clients:
                print "%s" % socket
                socket.send(text)
        print text