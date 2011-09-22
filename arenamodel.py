#!/usr/bin/env python
import cocos
import pyglet
import weakref

class ArenaModel(pyglet.event.EventDispatcher):
    """ Model (of the MVC pattern) """
    
    def move_left(self):
        self.dispatch_event("on_change_direction")
    
    def move_right(self):
        self.dispatch_event("on_change_direction")
            
    def move_down(self):
        self.dispatch_event("on_change_direction")
        
    def move_up(self):
        self.dispatch_event("on_change_direction")
        
    def set_controller( self, ctrl ):
        self.ctrl = weakref.ref(ctrl)

ArenaModel.register_event_type('on_change_direction')