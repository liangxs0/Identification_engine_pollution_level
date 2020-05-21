# coding: utf-8
'''
descrobe:zookeeper操作
author:lxs
date:2020-5-7
version:V1
'''
from kazoo.client import KazooClient
from mid_config_operator import config
import json

class CreateKazooNode(object):
    def __init__(self):
        self.kz_create = KazooClient(hosts=config.config["kazoo"]["KAZOO_HOST"])
    def create_node(self,node,data):
        self.kz_create.start()
        self.kz_create.create("/car_engine_app_test/{}".format(node),makepath=True)
        da = json.dumps(data).encode("utf-8")
        self.kz_create.set("/car_engine_app_test/{}".format(node),da)
        self.kz_create.stop()
class MidKazooClient(object):
    def __init__(self):
        self.zk_client = KazooClient(hosts=config.config["kazoo"]["KAZOO_HOST"])
    def kazoo_info_get(self):
        self.zk_client.start()
        self.nodes = self.zk_client.get_children(config.config["kazoo"]["KAZOO_ROOT"])
        for node in self.nodes:
            self.user_node = self.zk_client.get_children(config.config["kazoo"]["USER_NODE"].format(node))
            for nn in self.user_node:
                print(nn)
                print(config.config["kazoo"]["KAZOO_NODE"].format(node,nn))
                print(str(self.zk_client.get(config.config["kazoo"]["KAZOO_NODE"].format(node,nn))[0],encoding="utf-8").replace("null",""))
                # print(nn)

        self.zk_client.stop()
class MidKazooUpdate(object):
    def __init__(self):
        self.zk_update = KazooClient(hosts=config.config["kazoo"]["KAZOO_HOST"])
    def kazoo_info_update(self,node,data):
        self.zk_update.start()
        da = json.dumps(data).encode("utf-8")
        self.zk_update.set(node,da)
        self.zk_update.stop()
class MidKazooDel(object):
    def __init__(self):
        self.zk_del = KazooClient(hosts=config.config["kazoo"]["KAZOO_HOST"])
    def kazoo_delet(self):
        self.zk_del.start()
        self.nodes = self.zk_del.get_children("/car_engine_app_test")
        for node in self.nodes:
            print(self.zk_del.delete("/car_engine_app_test/{}".format(node)))
            print(node)
        self.zk_del.stop()

kazoo_client = MidKazooClient()
kazoo_update = MidKazooUpdate()

if __name__ == "__main__":
    #测试数据
    queue_config = {
        "task_type":0,#任务类型 0：初始化训练 1:优化训练 2:评估训练
        "task_id":2,#任务id
        "train_model_id":2,#训练模型id,
        "train_model_name":"NOZZLE_Name",#模型名称
        # "model_version":"V1",#如果要是初始化训练就是None
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
        "new_model_path":"a/b/c/d",#相对路径
        "train_dataset_id":[3,4,5],#训练数据集id
        "training_status":1 #训练状态
    }
    # cc = CreateKazooNode()
    # cc.create_node("0000-05-07 15:43:54.152928",queue_config)
    # client = MidKazooClient()
    # client.kazoo_info_get()
    # up = MidKazooUpdate()
    # up.kazoo_info_update("2020-05-07 15:43:54.152928",queue_config)
    client = MidKazooClient()
    client.kazoo_info_get()
    # dela = MidKazooDel()
    # dela.kazoo_delet()