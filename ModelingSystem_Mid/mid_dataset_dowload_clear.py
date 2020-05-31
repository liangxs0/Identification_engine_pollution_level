# coding: utf-8
'''
describe:数据集下载解码，清除
author:lxs
version:v2
date:2020
'''
import requests
import urllib
import os,shutil
import base64
from mid_config_operator import config
from mid_log_set import log
from mid_dir_operator import dir_operator
from mid_database_operate import dbase


class DatasetDowloadClear(object):
    def __init__(self):
        pass
    # def dowload_save_bs64(self,dataset_ids):
    #     if not dir_operator.create_dir(config.config["path"]["datasetdir_path"]):
    #         return False
    #     names = dbase.dataset_info_get(dataset_ids)
    #     if not names:
    #         return False
    #     if not dir_operator.create_first_dir(ids=dataset_ids,dataset_names=names):
    #         return False
    #     for id in dataset_ids:
    #         if not self.reponse_get(id):
    #             return False
    #         if self.response.json()["data"] == None:
    #             log.info("dataset {} is free".format(names[id]))
    #             continue
    #         if not dir_operator.create_second_tree(names,id,self.response):
    #             return False
    #         for tag in self.response.json()["data"]:
    #             for image in self.response.json()["data"][tag]:
    #                 if not dir_operator.image_save(names,id,self.response,tag,image):
    #                     return False
    #     return True
    # def reponse_get_bs64(self,id):
    #     self.response = requests.get(config.config["url"]["dataset_url"].format(id))
    #     if self.response.status_code > 200 and self.response.status_code < 200:
    #         log.error("dataset_{} response faile".format(id))
    #         return False
    #     return True
    def dowload_save_bytes(self,dataset_ids):
        for id in dataset_ids:
            if not self.reponse_get_bytes(id):
                log.error("dataset:{} dowload fail".format(id))
                return False
            with open(config.config["path"]["datasetdir_paths"].format(id),"ab") as f:
                # f.write(self.response_bytes.content)
                for chunk in self.response_bytes.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        return True
    def reponse_get_bytes(self,id):
        self.headers = {'content-type': 'application/json',
                        "authorization":"Bearer wYlvTrIhhvMpfBC4cW1Wdef4FoNgJt"}
        try:
            self.response_bytes = requests.get(config.config["url"]["dataset_url"].format(id),headers=self.headers,stream=True)
            if self.response_bytes.status_code > 200 and self.response_bytes.status_code < 200:
                log.error("dataset_{} response faile".format(id))
                return False
            return True
        except Exception as e:
            log.error("requests error %s"%e)
            return False

d_dataset = DatasetDowloadClear()

if __name__ == "__main__":
    DD = DatasetDowloadClear()
    print(DD.dowload_save_bytes([1,2,3]))
    # dir_operator.clear(config.config["path"]["datasetdir_path"])
