#!/usr/bin/env python
import cocos
import cocos.actions as ac
from cocos.director import director
import pyglet
import time

class ArenaView(cocos.layer.Layer):
    """ View  (of the MVC pattern) """
    
    messages = []
    
    def __init__(self, model, client, console):
        super(ArenaView,self).__init__()
        self.model = model
        self.client = client
        self.consolelayer = console
        self.model.push_handlers(self.on_local_change_direction)
        self.client.push_handlers(self.on_remote_connected)
        self.client.push_handlers(self.on_remote_disconnected)
        self.client.push_handlers(self.on_remote_change_direction)
        self.schedule(self.update_console)
        self.consolelayer.push_text("Welcome!")
        
    def update_console(self, dt):
        for msg in self.messages:
            self.consolelayer.push_text(msg)
            self.messages.remove(msg) #remove from the list

    def on_local_change_direction(self, direction):
        self.client.confobj.logger.debug("%s" % direction)
        
    def on_remote_change_direction(self, clientid, direction):
        self.client.confobj.logger.debug("%s - %s" % (clientid, direction))
        
    def on_remote_connected(self, clientid):
        self.client.confobj.logger.debug("%s" % clientid)
        self.messages.append("%d - %s \n ciao" % (time.time(), clientid))
        
    def on_remote_disconnected(self, clientid):
        self.client.confobj.logger.debug("%s" % clientid)

class ConsoleLayer(cocos.layer.Layer):
    
    labels = []
    
    def label(self):
        return cocos.text.Label("", font_size = 11, font_name = "Courier New", color = (0, 255, 0, 255))
    
    def __init__(self):
        super(ConsoleLayer, self).__init__()
    
    def push_text(self, text):
        label = self.label()
        label.element.text = text
        labels.insert(label, 0)
    
    def draw_labels(self):
        for i in range(3):
            