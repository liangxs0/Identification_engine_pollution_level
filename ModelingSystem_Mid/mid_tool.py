# coding: utf-8
import os
from mid_config_operator import config
os.system(
    "sqlacodegen --noviews --noconstraints --noindexes --outfile ./database_models_2.py mysql://{}:{}@{}:{}/{}".format(config.config["db1"]["db_user"],config.config["db1"]["db_psk"],
                                            config.config["db1"]["db_host"],config.config["db1"]["db_port"],
                                            config.config["db1"]["db_name"])
)