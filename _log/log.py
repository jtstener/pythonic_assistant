"""
File: log.py
Author: Julius Stener
Description: This file contains the Log class.
"""

# imports
import logging

class Log():
    """docstirng for the Log class, which is a simple wrapper around logging"""
    
    def __init__(self, **kwargs):
        """docstring for __init__ in the Log class"""
        
        # create the logger
        self.log_name = kwargs.get('log_name', 'assistant_log')
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(logging.DEBUG)

        # create the file handler
        self.log_filename = kwargs.get('log_filename', '_log/local.log')
        fh = logging.FileHandler(self.log_filename)
        fh.setLevel(logging.DEBUG)

        # create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self, msg):
        """"docstring for debug in the Log class"""
        self.logger.debug(msg)

    def info(self, msg):
        """"docstring for info in the Log class"""
        self.logger.info(msg)

    def warning(self, msg):
        """"docstring for warning in the Log class"""
        self.logger.warning(msg)

    def error(self, msg):
        """"docstring for error in the Log class"""
        self.logger.error(msg)

    def critical(self, msg):
        """"docstring for critical in the Log class"""
        self.logger.critical(msg)