#!/usr/bin/env python
import pyglet
import cocos
from cocos.director import director

class ArenaView(cocos.layer.Layer):
    """ View  (of the MVC pattern) """
    
    def __init__(self, model, client):
        super(ArenaView,self).__init__()
        self.model = model
        self.client = client
        self.model.push_handlers(self.on_local_change_direction)
        self.client.push_handlers(self.on_remote_connected)
        self.client.push_handlers(self.on_remote_disconnected)
        self.client.push_handlers(self.on_remote_change_direction)
        self.add(LogLayer())
        
    def on_local_change_direction(self, direction):
        self.client.confobj.logger.debug("%s" % direction)
        return True
        
    def on_remote_change_direction(self, clientid, direction):
        self.client.confobj.logger.debug("%s - %s" % (clientid, direction))
        return True
        
    def on_remote_connected(self, clientid):
        self.client.confobj.logger.debug("%s" % clientid)
        return True
        
    def on_remote_disconnected(self, clientid):
        self.client.confobj.logger.debug("%s" % clientid)
        return True

class LogLayer(cocos.layer.Layer):
    
    def __init__(self):
        super(LogLayer, self).__init__()
        w,h = director.get_window_size()
        
    def draw(self):
        super(LogLayer, self).draw()