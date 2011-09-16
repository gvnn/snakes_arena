import ConfigParser
import string

config_values = {
    "server" : {
        "port" : "41414",
        "host" : "localhost"
        }
    }

def load_config():
    """
    returns a dictionary with key's of the form
    <section>.<option> and the values 
    """
    file = "config.ini"
    config = {}
    cp = ConfigParser.ConfigParser()
    cp.read(file)
    for sec in cp.sections():
        name = string.lower(sec)
        config[name] = {}
        for opt in cp.options(sec):
            config[name][string.lower(opt)] = string.strip(cp.get(sec, opt))
    config_values = config