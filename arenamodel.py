#!/usr/bin/env python
import cocos
import pyglet
import weakref

class ArenaModel(pyglet.event.EventDispatcher):
    """ Model (of the MVC pattern) """
    
    def __init__(self):
        self._remote_clients = []
    
    def append_client(self, clientid):
        self._remote_clients.append(clientid)
    
    def remove_client(self, clientid):
        self._remote_clients.remove(clientid)
    
    def move_left(self):
        self.dispatch_event("on_local_change_direction", "left")
    
    def move_right(self):
        self.dispatch_event("on_local_change_direction", "right")
            
    def move_down(self):
        self.dispatch_event("on_local_change_direction", "down")
        
    def move_up(self):
        self.dispatch_event("on_local_change_direction", "up")
        
    def set_controller(self, ctrl):
        self.ctrl = weakref.ref(ctrl)

ArenaModel.register_event_type('on_local_change_direction')