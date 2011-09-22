#!/usr/bin/env python
import sys
import argparse
import config
import server
import client
import threading
import cocos
import arena
import time

confobj = None #: config object

def start_server(ip = "", port = 0):
    """ starts a new snake game server """
    if ip == "" or port == 0:
        print("Choose one of your network interfaces:")
        interfaces_ips = server.get_available_ips()
        #enumerates all the interfaces, displays only the ones with an ip
        for i, interface in enumerate(interfaces_ips):
            print("\t %(num)s. %(ip)s" % {"num" : i, "ip" : interface})
        netnum = raw_input("Enter net number: ")
        confobj.logger.info("net chosen %s" % netnum);
    #setting up the server
    s = server.SnakeServer(ip, port, confobj)
    #start the thread
    t = threading.Thread(target=s.start)
    t.setDaemon(True)
    t.start()
    
def start_client(ip = "", port = 0):
    if ip == "" or port == 0:
        ip = raw_input("Enter server\'s ip address (127.0.0.1): ")
        port = raw_input("Enter server\'s TCP port (%s): " % confobj.settings["server"]["port"])
        if port == "":
            port = int(conf.settings["server"]["port"])
        if ip == "":
            ip = "127.0.0.1"
    return client.SnakeClient(ip, port, confobj)

def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', action='store', dest='mode', default="", help='game mode: SERVER or CLIENT')
    parser.add_argument('-s', action='store', dest='server_ip', default="", help='server ip')
    parser.add_argument('-p', action='store', dest='server_port', default=0, help='server port', type=int)
    results = parser.parse_args()
    print("Welcome reptile!")
    mode = ""
    if results.mode:
        mode = results.mode.upper()
    else:
        mode = raw_input("do you want to be SERVER or a CLIENT? ").upper()
    if mode in ['SERVER', 'CLIENT']:
        confobj.logger.info("mode chosen %s" % mode)
        if mode == "SERVER":
            #start a new server
            start_server(results.server_ip, results.server_port)
        #new client
        c = None
        try:
            c = start_client(results.server_ip, results.server_port)
            pass
        except Exception, e:
            time.sleep(1)
            c = start_client(results.server_ip, results.server_port)
        #starting a new game
        cocos.director.director.init(resizable=False, width=600, height=600)
        cocos.director.director.run(arena.newgame(c))
        if mode == "CLIENT":
            #send client leaving
            c.send_command("q")

if __name__ == "__main__":
    #load configs
    confobj = config.Config()
    confobj.logger.info("configuration loded")
    #start program
    main()