#!/usr/bin/env python
import cocos
import pyglet

class ArenaView(cocos.layer.Layer):
    """ View  (of the MVC pattern) """
    
    def __init__(self, model, client):
        super(ArenaView,self).__init__()
        self.model = model
        self.client = client
        self.model.push_handlers(self.on_change_direction)
        
    def on_change_direction(self):
        return True