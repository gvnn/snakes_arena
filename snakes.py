#!/usr/bin/env python
import config
import netifaces

def start_server():
    """docstring for start_server"""
    print("Choose one of your network interfaces")
    for i, interface in enumerate(netifaces.interfaces()):
        ifaddresses = netifaces.ifaddresses(str(interface))
        if netifaces.AF_INET in ifaddresses:
            print("%(num)s. %(name)s - %(ip)s" % {"num" : i, "name" : interface, "ip" : ifaddresses[netifaces.AF_INET][0]["addr"]})
    netnum = raw_input("Enter net number:")
    conf.logger.info("net chosen %s" % netnum);
    
def start_client():
    """docstring for start_client"""

if __name__ == "__main__":
	#load configs
	conf = config.Config()
	conf.logger.info("configuration loded")
	
	#game mode option
	print("Welcome reptile,")
	mode = raw_input("do you want to be SERVER or a CLIENT?").upper()
	if mode in ['SERVER', 'CLIENT']:
	    conf.logger.info("mode chosen %s" % mode);
	    if mode == "SERVER":
	        start_server()
	    else:
	        start_client()
	    