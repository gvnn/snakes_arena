#!/usr/bin/env python
import config
import server
import client
import threading
import cocos
import arena

conf = None #config obj

def start_server():
    """ starts a new snake game server """
    print("Choose one of your network interfaces:")
    interfaces_ips = server.get_available_ips()
    #enumerates all the interfaces, displays only the ones with an ip
    for i, interface in enumerate(interfaces_ips):
        print("\t %(num)s. %(ip)s" % {"num" : i, "ip" : interface})
    netnum = raw_input("Enter net number: ")
    conf.logger.info("net chosen %s" % netnum);
    #setting up the server
    server.conf = conf
    server_address = (interfaces_ips[int(netnum)], int(conf.settings["server"]["port"]))
    s = server.SnakeServer(server_address, server.SnakeRequestHandler)
    #start the thread
    t = threading.Thread(target=s.serve_forever)
    t.setDaemon(True)
    t.start()
    return s

def start_client():
    """ starts a new client session """
    ip = raw_input("Enter server\'s ip address (127.0.0.1): ")
    port = raw_input("Enter server\'s UDP port (%s): " % conf.settings["server"]["port"])
    if port == "":
        port = int(conf.settings["server"]["port"])
    if ip == "":
        ip = "127.0.0.1"
    #setting up the client
    client.conf = conf
    c = client.SnakeClient(ip, port)
    t = threading.Thread(target=c.connect)
    t.setDaemon(True)
    t.start()
    return c

if __name__ == "__main__":
    #load configs
    conf = config.Config()
    conf.logger.info("configuration loded")
    #game mode option
    print("Welcome reptile,")
    mode = raw_input("do you want to be SERVER or a CLIENT? ").upper()
    if mode in ['SERVER', 'CLIENT']:
        conf.logger.info("mode chosen %s" % mode)
        s = None
        ss = None
        if mode == "SERVER":
            ss = start_server()
        else:
            s = start_client()
        
        cocos.director.director.init()
        arena_layer = arena.Arena()
        
        if s:
            arena_layer._tmp_socket = s
        if ss:
            arena_layer._tmp_server_socket = ss
            
        main_scene = cocos.scene.Scene(arena_layer)
        cocos.director.director.run(main_scene)