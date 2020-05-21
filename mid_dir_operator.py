# coding: utf-8
'''
describe:文件夹的创建和文的删除
author :lxs
date:2020
version:V2
'''
import os,shutil,sys,zipfile,io
import re
from mid_config_operator import config
from mid_database_operate import dbase
from mid_log_set import log
import base64


class DirOperator(object):
    def __init__(self):
        self.create_dir(config.config["path"]["datasetdir_path"])
    def create_second_tree(self,dataset_names,id,response):
        if not id in list(dataset_names.keys()):
            return False
        for tag in response.json()["data"]:
            if not self.create_dir(config.config["path"]["seconddir_path"].format(dataset_names[id],id,tag)):
                return False
        return True
    def create_first_dir(self,dataset_names,ids):
        for id in ids:
            if id in list(dataset_names.keys()):
                if not self.create_dir(config.config["path"]["firstdir_path"].format(dataset_names[id],id)):
                    log.error("file {} create faile".format(dataset_names[id]))
                    return False
        return True
    def image_save(self,dataset_names,id,response,tag,image):
        try:
            with open(config.config["path"]["image_path"].format(dataset_names[id],id,tag,image),"wb+") as f:
                f.write(base64.b64decode(response.json()["data"][tag][image]))
                f.close()
        except Exception as e:
            log.error("image:{} svase error  {}".format(image,e))
            return False
        return True
    def clear(self,path):
        try:
            shutil.rmtree(path)
            return True
        except Exception as e:
            log.error("del file error:{}".format(e))
            return False
    def create_dir(self,path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
                return True
            except Exception as e:
                log.error(e)
                return False
        return True
    def un_zip(self,zip_file_name):
        self.cur_path = os.path.dirname(os.path.realpath(__file__))
        d_path = config.config["path"]["datasetdir_path"].replace("./","")
        self.zip_path = os.path.join(self.cur_path,d_path,zip_file_name)
        self.tar_path = os.path.join(self.cur_path,d_path)
        z = zipfile.ZipFile(self.zip_path,"r")
        for k in z.infolist():
            try:
                save_path = (self.tar_path+"/"+k.filename).replace("\\","/")
                if not os.path.exists(save_path):
                    if not "." in save_path:
                        os.mkdir(save_path)
                if "." in save_path:
                    image_file = z.read(k)
                    with open(save_path,"wb") as f:
                        f.write(image_file)
            except Exception as e:
                log.error("image unzip fail {}".format(e))
                return False 
        z.close()
        return True
    def unzip_all(self):
        for dir in os.listdir(config.config["path"]["datasetdir_path"]):
            if ".zip" in dir:
                self.un_zip(dir)
        return True
    def dataset_path_get(self):
        try:
            self.cur_path = os.path.dirname(os.path.realpath(__file__))
            return [os.path.join(self.cur_path,dir) for dir in os.listdir(config.config["path"]["datasetdir_path"]) if not ".zip" in dir]  
        except Exception as e:
            log.error("dataset path get fail {}".format(e))
            return False 

dir_operator = DirOperator()


if __name__ == "__main__":
    dir_operator.unzip_all()
    print(dir_operator.dataset_path_get())
   
    