# coding: utf-8
'''
describe:指标计算
author:lxs
version:V2
date:2020
'''
import time
from  mid_database_operate import dbase
import os
#测试数据
data_re = {
        "training_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "accuracy_rate":90.0,
        "model_version":"V14",
        "model_fileaddr":"http:/*?/",
        "dataset_list":"1,2,3",
        "training_model_id":2,
        "tags_index":[
            {"F1score":2.0,"Gscore":3.0,"precision_rate":4.0,"recall_rate":90.0,"label_id":1},
            {"F1score":3.0,"Gscore":4.0,"precision_rate":5.0,"recall_rate":93.0,"label_id":2},
            {"F1score":4.0,"Gscore":5.0,"precision_rate":6.0,"recall_rate":94.0,"label_id":3},
            {"F1score":5.0,"Gscore":6.0,"precision_rate":7.0,"recall_rate":95.0,"label_id":4},
        ],
        "error_images":[
            {"pic_address":"dasdad0","old_label":"严重","new_label":"重度"},
            {"pic_address":"dasdad1","old_label":"严重","new_label":"重度"},
            {"pic_address":"dasdad2","old_label":"严重","new_label":"重度"},
            {"pic_address":"dasdad3","old_label":"严重","new_label":"重度"},
            {"pic_address":"dasdad4","old_label":"严重","new_label":"重度"},
            {"pic_address":"dasdad5","old_label":"严重","new_label":"重度"},
        ]
    }


class Calculation(object):
    def get_result(self,data,task_type):
        if task_type is 2:
            return data_re
        # index_calculation(model_file_path,dataset_path)
        if task_type is 0:
            ver = None
        if task_type is 1:
            ver = data["model_version"]
        data_re["training_time"] = data["training_time"]
        data_re["model_version"] = self.version_get(data["train_model_id"],ver)
        data_re["training_model_id"] = data["train_model_id"]
        data_re["dataset_list"] = str(data["train_dataset_id"]).replace("[","").replace("]","")
        if not task_type is 2:
            data_re["model_fileaddr"] = "/{}/{}.h5".format(os.path.split(data["new_model_path"])[1],data["train_model_name"])
        return data_re
    def version_get(self,model_id,version):
        res = dbase.model_info_get(model_id,version)
        if res[2] == None:
            return "V1"
        else:
            return ("V{}".format(int(res[2].model_version.replace("V",""))+1))
            

cal_result = Calculation()

if __name__ == "__main__":
    a = os.path.split("a:/n/c/c/d/a")
    print(a[1])