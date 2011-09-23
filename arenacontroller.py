#!/usr/bin/env python
import cocos
import pyglet
from pyglet.window import key

class ArenaController(cocos.layer.Layer):
    """ Controller ( MVC ) """
    is_event_handler = True #: enable pyglet's events
    
    def __init__(self, model, client):
        super(ArenaController, self).__init__()
        self.model = model
        self.client = client
        
    def on_key_press (self, k, m):
        if k in (key.LEFT, key.RIGHT, key.DOWN, key.UP):
            if k == key.LEFT:
                self.client.send_command("left")
                self.model.move_left()
            elif k == key.RIGHT:
                self.client.send_command("right")
                self.model.move_right()
            elif k == key.DOWN:
                self.client.send_command("down")
                self.model.move_down()
            elif k == key.UP:
                self.client.send_command("up")
                self.model.move_up()
            return True
        return False