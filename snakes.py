#!/usr/bin/env python
import config
import server
import client
import netifaces
import threading

conf = None #config obj

def start_server():
    """ starts a new snake game server """
    print("Choose one of your network interfaces:")
    interfaces_ips = {}
    #enumerates all the interfaces, displays only the ones with an ip
    for i, interface in enumerate(netifaces.interfaces()):
        ifaddresses = netifaces.ifaddresses(str(interface))
        if netifaces.AF_INET in ifaddresses:
            interfaces_ips[str(i)] = ifaddresses[netifaces.AF_INET][0]["addr"]
            print("\t %(num)s. %(name)s - %(ip)s" % {"num" : i, "name" : interface, "ip" : ifaddresses[netifaces.AF_INET][0]["addr"]})
    netnum = raw_input("Enter net number: ")
    conf.logger.info("net chosen %s" % netnum);
    #setting up the server
    server.conf = conf
    server_address = (interfaces_ips[netnum], int(conf.settings["server"]["port"]))
    s = server.SnakeServer(server_address, server.SnakeRequestHandler)
    #start the thread
    t = threading.Thread(target=s.serve_forever)
    t.setDaemon(True)
    t.start()
    
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

if __name__ == "__main__":
	#load configs
	conf = config.Config()
	conf.logger.info("configuration loded")
	
	#game mode option
	print("Welcome reptile,")
	mode = raw_input("do you want to be SERVER or a CLIENT? ").upper()
	if mode in ['SERVER', 'CLIENT']:
	    conf.logger.info("mode chosen %s" % mode);
	    if mode == "SERVER":
	        start_server()
	    else:
	        start_client()
	raw_input("\npress any key to exit\n")