#!/usr/bin/env python
import cocos
import pyglet
import arenaview
import arenacontroller
import arenamodel

def newgame(client):
    """returns the game scene"""
    scene = cocos.scene.Scene()
    model = arenamodel.ArenaModel() # model
    ctrl = arenacontroller.ArenaController(model, client) # controller
    view = arenaview.ArenaView(model, client) # view
    # set controller in model
    model.set_controller(ctrl)
    # add controller
    scene.add(ctrl, z=0, name="controller")
    # add view
    scene.add(view, z=1, name="view")
    return scene