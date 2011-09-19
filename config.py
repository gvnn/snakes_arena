#!/usr/bin/env python
import ConfigParser
import string
import logging
import logging.config

class Config:
    
    """ game settings dict """
    _settings = None
    
    """ standard python logger """
    _logger = None
    
    def __init__(self):
        self.load_logger()
        self.load_config()
    
    @property
    def settings(self):
        return self._settings
    
    @property
    def logger(self):
        return self._logger

    def load_logger(self):
        """loads logging configurations"""
        logging.config.fileConfig('logging.ini')
        # create logger
        self._logger = logging.getLogger('snake')
        if self._logger:
            self._logger.debug("logger loaded")

    def load_config(self):
        """
        returns a dictionary with key's of the form
        { <section> : { <option> : <value> } ... }
        """
        config_settings = {}
        cp = ConfigParser.ConfigParser()
        cp.read("config.ini")
        for sec in cp.sections():
            name = string.lower(sec)
            config_settings[name] = {}
            for opt in cp.options(sec):
                config_settings[name][string.lower(opt)] = string.strip(cp.get(sec, opt))
        if config_settings:
            self._logger.debug("settings loaded")
            self._settings = config_settings