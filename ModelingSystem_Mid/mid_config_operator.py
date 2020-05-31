# coding: utf-8
import configparser
import os

class ConfigOperator(object):
    def __init__(self):
        #获取文件的当前路径（绝对路径）
        self.cur_path = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(self.cur_path,"mid_config.cfg")
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

config = ConfigOperator()
