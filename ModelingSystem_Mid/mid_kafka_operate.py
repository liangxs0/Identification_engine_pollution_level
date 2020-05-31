# coding: utf-8

'''
describe:kafka的操作
author:lxs
date:2020-4-29
version:V3
'''


from kafka import KafkaProducer,KafkaConsumer,KafkaClient
from kafka.errors import KafkaError
import json,ast
import sys,time
from mid_log_set import log
from mid_config_operator import config

# KAFAKA_HOST = "172.16.0.4"
# KAFAKA_PORT = 9092
# KAFAKA_TOPIC = "carengine_test0"

class MidKafkaProducer():
    def __init__(self, kafkahost,kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                kafka_host=self.kafkaHost,
                kafka_port=self.kafkaPort
                )
        self.producer = KafkaProducer(bootstrap_servers = [bootstrap_servers])

    def sendjsondata(self, params, key):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            v = parmas_message.encode('utf-8')
            producer.send(self.kafkatopic,value= v,key=key.encode("utf-8"))
            producer.close()
            return True
        except KafkaError as e:
            log.error("kafka input data failed {}".format(e))
            return False

class MidKafkaConsumer():
    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                kafka_host=self.kafkaHost,
                kafka_port=self.kafkaPort
                )
        self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,bootstrap_servers = [bootstrap_servers])

    # def consume_data(self):
    #     try:
    #         for message in self.consumer:
    #             self.consumer.poll(timeout_ms=1000)
    #             yield message
    #     except KeyboardInterrupt as e:
    #         log.error("kafka consumer error {}".format(e))

if __name__ == "__main__":
    queue_config = {
        "task_type":0,#任务类型 0：初始化训练 1:优化训练 2:评估训练
        "task_id":1,#任务id
        "train_mode_id":3,#训练模型id,
        "train_model_name":"NOZZLE_Name",#模型名称
        "model_version":"Non",#如果要是初始化训练就是None
        "part_name":"NOZZLE",
        #注意：如果训练类型为1或者2时不需要指定参数，数据写入None即可
        "reslution":"320x240",#分辨率
        "iterate_times":100,#迭代次数
        "network_structure":"AAA",#网络结构
        "optimizer":"BBB",#优化器
        "loss_value":"CCCC",#损失值
        "callback":["4","5","3"],#回调函数
        "measure":["11","22","33"],#度量器
        #注意：评估不需要指定模型的存放地址，为None即可
        "new_model_path":"new_model_path",#相对路径
        "train_dataset_id":[1,2,3],#训练数据集id
    }
    
   
    # while True:
    #     pro = MidKafkaProducer(config.config["kafka"]["KAFKA_HOST"],config.config["kafka"]["KAFKA_PORT"],
    #                             config.config["kafka"]["KAFKA_TOPIC"])
    #     print(pro.sendjsondata(queue_config,"carengine_test0"))
        # time.sleep(1)
        # con = MidKafkaConsumer(KAFAKA_HOST,KAFAKA_PORT,KAFAKA_TOPIC,"carengine_test0")
        # print(con.consume_data())
    #     con = MidKafkaConsumer(KAFAKA_HOST,KAFAKA_PORT,KAFAKA_TOPIC,"carengine_test0")
    #     msg = con.consumer.poll(timeout_ms=5)
    #     if msg is None:
    #         continue
    #     else:
    #         print(msg)
    #         print(type(msg))
    #         time.sleep(0.5)

    con = MidKafkaConsumer(config.config["kafka"]["KAFKA_HOST"],config.config["kafka"]["KAFKA_PORT"],
                                config.config["kafka"]["KAFKA_TOPIC"],config.config["kafka"]["KAFKA_GROUP"])
    msg = con.consumer
    for m in msg:
        print("-"*30)
        print(m.offset)
        data = str(m.value,encoding="utf-8")
        print(data)
        data = ast.literal_eval(data)
        for d in data["train_dataset_id"]:
            print(d)
            print(type(d))
            print(data["model_version"])
            print(type(data["model_version"]))


    