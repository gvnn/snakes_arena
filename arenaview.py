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
        self.messages.append("%d - %s" % (time.time(), clientid))
        
    def on_remote_disconnected(self, clientid):
        self.client.confobj.logger.debug("%s" % clientid)

class ConsoleLayer(cocos.layer.Layer):
    
    labelslist = []
    labelindex = 0;
    
    def label(self, text):
        return cocos.text.Label(text, font_size = 11, font_name = "Courier New", color = (0, 255, 0, 255), position = (5, -7))
    
    def __init__(self):
        super(ConsoleLayer, self).__init__()
        w,h = director.get_window_size()
        self.add(cocos.draw.Line(start=(0,60), end=(w,60), color=(0, 255, 0, 255)), "console_delimiter")
    
    def push_text(self, text):
        #For some reason the push and pop in the children list of the layer looks completely random
        #I'm keeping a dictionary of labels
        label = self.label(text)
        label_name = "row%d" % self.labelindex
        
        if len(self.labelslist) > 3:
            label_to_remove = self.labelslist.pop(0)
            self.remove(label_to_remove)
            
        self.labelslist.append(label_name)
        self.labelindex += 1
        self.add(label, name = label_name)
        self.move_labels()
        
    def move_labels(self):
        for idx, label in enumerate(self.labelslist):
            self.get(label).do(ac.MoveBy((0, 12), duration=0.3))