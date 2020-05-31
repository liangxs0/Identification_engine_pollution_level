# coding: utf-8
'''
describe: 任务分配和执行数据保存
author:lxs
version:v3
date:2020-4-28
'''
from mid_kafka_operate import MidKafkaConsumer
from mid_config_operator import config
from mid_model_train import model_train
from mid_database_operate import dbase
from mid_log_set import log
from mid_dir_operator import dir_operator
from mid_dataset_dowload_clear import d_dataset
from mid_kazoo_operator import kazoo_client,kazoo_update
from mid_calculation import cal_result
import ast
import time

class Master(object):
    def str_dict(self,d_str):
        try:
            dic = ast.literal_eval(d_str)
            return dic
        except Exception as e:
            log.error("String conversion dictionary faile {}".format(e))
            return False
    def task_allocation_kazoo(self):
        kazoo_client.zk_client.start()
        for node in kazoo_client.zk_client.get_children(config.config["kazoo"]["KAZOO_ROOT"]):
            self.user_node = kazoo_client.zk_client.get_children(config.config["kazoo"]["USER_NODE"].format(node))
            for nn in self.user_node:
                try:
                    d_data = ast.literal_eval(str(kazoo_client.zk_client.get(config.config["kazoo"]["KAZOO_NODE"].format(node,nn))[0],encoding="utf-8").replace("null","None"))
                    if len(d_data) is 0:
                        break
                    d_data["task_type"] = int(d_data["task_type"])
                    if d_data["training_status"] is 4 or d_data["training_status"] is 5 \
                    or d_data["training_status"] is 8 or d_data["training_status"] is 9 \
                    or d_data["training_status"] is 12 or d_data["training_status"] is 13:
                        print("task is trained")
                        continue
                    else:
                        print("-"*10)
                        print("task type {}".format(d_data["task_type"]))
                        #数据拼接{
                        d_data.update({"training_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
                        self.t_data = self.train_parameter(d_data)
                        self.t_data = self.update_status(self.t_data,4,self.user_node,nn,self.t_data["train_model_id"])
                        self.t_data = self.update_status(self.t_data,4,self.user_node,nn,self.t_data["train_model_id"])
                        #进入训练
                        print("running task {}".format(node))
                        t_f = self.mid_train_switch(self.t_data["task_type"],self.t_data)
                        if not t_f:
                            self.update_status(self.t_data,4,self.user_node,nn,self.t_data["train_model_id"])
                            log.error("Abnormal end of training id {}".format(node))
                            print("error task {}".format(node))
                            break
                        self.res = cal_result.get_result(self.t_data,self.t_data["task_type"])
                        self.train_result_save_switch(self.t_data["task_type"],self.res,node)
                        print("end  task true{}".format(node))
                        dir_operator.clear(config.config["path"]["datasetdir_path"])
                        dir_operator.clear(config.config["path"]["all_dataset_dir_path"])
                        dir_operator.create_dir(config.config["path"]["datasetdir_path"])
                        dir_operator.create_dir(config.config["path"]["all_dataset_dir_path"])
                        self.update_status(self.t_data,4,self.user_node,nn,self.t_data["train_model_id"])
                        print("running end",True)
                        break
                except Exception as e:
                    log.error(e)
                    continue
    def mid_train_switch(self,task_type,data):
        if task_type == 0:
            return model_train.mid_model_init_train(data)
        elif task_type == 1:
            return model_train.mid_model_opt_train(data)
        elif task_type == 2:
            return model_train.mid_model_ass_train(data)
        else:
            log.error("fail task_type")
            return False
    def train_parameter(self,data):
        self.parameter = data
        #数据集下载
        if not d_dataset.dowload_save_bytes(self.parameter["train_dataset_id"]):
            log.error("Data set download failed")
            return False
        if not dir_operator.unzip_all():
            log.error("File unzip failed")
            return False
        # dataset_path = dir_operator.dataset_path_get()
        dataset_path = config.config["path"]["all_datasetfiles"]
        if not dataset_path:
            log.error("File address acquisition failed")
            return False
        self.parameter.update({"dataset_path":dataset_path})
        if self.parameter["task_type"] is 0:
            self.parameter_model_version = None
            self.parameter.update({"model_version":self.parameter_model_version})
            n_model_file_path = dbase.model_info_get(self.parameter["train_model_id"],self.parameter["model_version"])
            if n_model_file_path[2] is None:
                self.parameter_model_version = None
            self.parameter["model_version"] = self.parameter_model_version
            # self.parameter.update({"model_file_path":n_model_file_path[2].model_fileaddr})
            self.parameter["train_model_name"] = (self.parameter["train_model_name"] + "_{}".format(cal_result.version_get(self.parameter["train_model_id"],self.parameter["model_version"])))
            dir_operator.create_model_save_dir("/{}/{}".format(os.path.split(self.parameter["new_model_path"])[1],self.parameter["train_model_name"]))
        elif self.parameter["task_type"] is 1:
            n_model_file_path = dbase.model_info_get(self.parameter["train_model_id"],self.parameter["model_version"])
            if n_model_file_path[2] is None:
                log.error("Models cannot be optimized without training")
                return False
            self.parameter.update({"model_file_path":n_model_file_path[1].model_fileaddr})
            self.parameter["train_model_name"] = self.parameter["train_model_name"] + "_{}".format(cal_result.version_get(self.parameter["train_model_id"],self.parameter["model_version"]))
            dir_operator.create_model_save_dir("/{}/{}".format(os.path.split(self.parameter["new_model_path"])[1],self.parameter["train_model_name"]))
        elif self.parameter["task_type"] is 2:
            n_model_file_path = dbase.model_info_get(self.parameter["train_model_id"],self.parameter["model_version"])
            if n_model_file_path[2] is None:
                log.error("Models cannot be evaluated without training")
                return False
            self.parameter.update({"model_file_path":n_model_file_path[1].model_fileaddr})
        else:
            log.error("Wrong type of training")
            return False
        return self.parameter
    def train_result_save_switch(self,task_type,data,node):
        if task_type is 0 or task_type is 1 :
            if not dbase.insert_init_opt_result_save(data):
                log.error("init opt result save error {}".format(node))
                self.update_status(data,4,node,data["train_model_id"])
                return False
            return True
        elif  task_type is 2:
            if not dbase.insert_ass_result_save(data):
                log.error("ass result save error {}".format(node))
                self.update_status(data,4,node,data["train_model_id"])
                return False   
            return True            
        else:
            return False
    def update_status(self,data,status,user_node,node,model_id):
        if data["task_type"] is 0:
            if status is 1:
                data["training_status"] = int(config.config["status"]["INIT_STATU_READY"])
                
            elif status is 2:
                data["training_status"] = int(config.config["status"]["INIT_STATU_RUN"])
                
            elif status is 3:
                data["training_status"] = int(config.config["status"]["INIT_STATU_OK_END"])
                
            elif status is 4:
                data["training_status"] = int(config.config["status"]["INIT_STATU_NO_END"])
                
        elif data["task_type"] is 1:
            if status is 1:
                data["training_status"] = int(config.config["status"]["OPT_STATU_READY"])
                
            elif status is 2:
                data["training_status"] = int(config.config["status"]["OPT_STATU_RUN"])
                
            elif status is 3:
                data["training_status"] = int(config.config["status"]["OPT_STATU_OK_END"])
                
            elif status is 4:
                data["training_status"] = int(config.config["status"]["OPT_STATU_NO_END"])
                
        elif data["task_type"] is 2:
            if status is 1:
                data["training_status"] = int(config.config["status"]["ASS_STATU_READY"])
                
            elif status is 2:
                data["training_status"] = int(config.config["status"]["ASS_STATU_RUN"])
                
            elif status is 3:
                data["training_status"] = int(config.config["status"]["ASS_STATU_OK_END"])
                
            elif status is 4:
                data["training_status"] = int(config.config["status"]["ASS_STATU_NO_END"])
        else:
            return False
        kazoo_update.kazoo_info_update(config.config["kazoo"]["KAZOO_NODE"].format(user_node,node),data)
        dbase.updata_train_mdoel_status(model_id,data["training_status"])
        return data
runing = Master()
if __name__ == "__main__":
    queue_config = {
        "task_type":2,#任务类型 0：初始化训练 1:优化训练 2:评估训练
        "task_id":1,#任务id
        "train_model_id":1,#训练模型id,
        "train_model_name":"NOZZLE_Name",#模型名称
        "model_version":"V1",#如果要是初始化训练就是None
        "part_name":"NOZZLE",
        #注意：如果训练类型为1或者2时不需要指定参数，数据写入None即可
        "reslution":"320x240",#分辨率
        "iterate_times":100,#迭代次数
        "network_structure":"AAA",#网络结构
        "optimizer":"BBB",#优化器
        "loss_value":"CCCC",#损失值
        "callback":["1","2","3"],#回调函数
        "measure":["11","22","33"],#度量器
        #注意：评估不需要指定模型的存放地址，为None即可
        "new_model_path":"new_model_path",#相对路径
        "train_dataset_id":[3],#训练数据集id
        "training_statu":0 #训练状态
    }
    # s = Master()
    # # print(s.train_parameter(queue_config))
    # s.task_allocation_kazoo()