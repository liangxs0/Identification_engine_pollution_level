# coding: utf-8
'''
describe:日志配置
author:lxs
version:V2
date:2020
'''

import logging
from logging import handlers
 
 
class Logger(object):
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
 
    def __init__(self, filename="mid_log.log", level="info", when="D", backupCount=3, fmt="%(asctime)s - %(pathname)s[line:%(lineno)d] - %"
                                                                                              "(levelname)s: %(message)s"):
        format_str = logging.Formatter(fmt)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(format_str)
        fileHandler = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount, encoding="utf-8")
        fileHandler.setFormatter(format_str)
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(self.level_relations.get(level))
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)
log = Logger(level="debug").logger
