#!/usr/bin/env python
import cocos
import pyglet
import arenaview
import arenacontroller
import arenamodel

def newgame(client):
    """returns the game scene"""
    scene = cocos.scene.Scene()
    console = arenaview.ConsoleLayer()
    model = arenamodel.ArenaModel() # model
    ctrl = arenacontroller.ArenaController(model, client) # controller
    view = arenaview.ArenaView(model, client, console) # view
    # set controller in model
    model.set_controller(ctrl)
    # add controller
    scene.add(ctrl, z = 1, name = "controller")
    # add view & console
    scene.add(console, z = 3, name = "console")
    scene.add(view, z = 2, name = "view")
    return scene