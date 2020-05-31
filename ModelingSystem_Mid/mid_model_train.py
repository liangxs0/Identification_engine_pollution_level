# -*- coding:utf-8 -*-
'''
describe:训练任模块
author:lxs
version:v2
date:2020class
'''
from __future__ import absolute_import, division, print_function, unicode_literals
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import shutil
import json
import pandas as pd
import os
import keras
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.resnet50 import ResNet50
from keras import layers
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten,GlobalAveragePooling2D,GlobalMaxPooling2D
from keras import backend as K


from mid_config_operator import config
from mid_log_set import log
import re
from mid_dir_operator import dir_operator

class ModelTrain(object):
    def __init__(self):
        pass
    def mid_height_width(self,parameter):
        res = re.findall("([1-9]\d*)x([1-9]\d*)",parameter["reslution"])
        return int(res[0][0]),int(res[0][1])
    def mid_reflect(self,class_name,method,*arg):
        self.dd = __import__(class_name,fromlist = True)    
        self.fun = getattr(self.dd,method)
        if len(arg[0]) != 0:
            return self.fun(*arg)
        else:
            return self.fun
       
    def gpu_init(self,memory_size):
        #gpu启动控制
        tf.config.set_soft_device_placement(True)
        gpus = tf.config.experimental.list_physical_devices('GPU')
        tf.config.experimental.set_visible_devices(devices=gpus[0], device_type='GPU')
        tf.config.experimental.set_memory_growth(gpus[0], True)
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_size)])
    def mid_create_model(self,parameter):
        try:
            image_height, image_width = self.mid_height_width(parameter)
            dd = [False,None,(image_height, image_width,3)]
            self.c_conv_base = self.mid_reflect("keras.applications.resnet","ResNet50",dd)
            # self.c_conv_base = keras.applications.resnet50.ResNet50(include_top=False, weights='imagenet',input_shape=(image_height, image_width,3))
            self.x = self.c_conv_base.output
            self.x = Flatten()(self.x)
            self.x = Dense(64,activation="relu")(self.x)
            self.x = Dense(len(parameter["target"]),activation="softmax")(self.x)
            self.c_model = Model(inputs=self.c_conv_base.input,outputs=self.x)
            return True,self.c_model
        except Exception as e:
            log.error("create model error {}".format(e))
            return False,None

    def mid_model_callback(self,model_path,result_path):
        check_path = os.path.join(MODEL_PATH,'checkpoint')
        dir_operator.create_model_save_dir(check_path)
        check_dir = os.path.dirname(check_path)
        self.m_m_cp_callbacks = [
        keras.callbacks.ModelCheckpoint(
            check_path,  
            verbose=1, 
            monitor='val_loss',
            save_best_only=True,
            save_weights_only = True
        ),
        history_pic(result_path, []),
        keras.callbacks.EarlyStopping(
            monitor='val_loss', mode='min', 
            patience=50,
            verbose=0,
            restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.1, 
            patience=3,
            verbose=1
            )
    ]

        return self.m_cp_callbacks
    def mid_package_program(self,parameter):
        try:
            image_height,image_width = self.mid_height_width(parameter)
            self.flag,self.m_model = self.mid_create_model(parameter)#这个地方后面要修改
            print("-"*10)
            self.m_loss = self.mid_reflect(parameter["loss_value"],"SparseCategoricalCrossentropy",[])()#损失函数这个返回的是类加()获取对象
            self.m_optimizer = self.mid_reflect(parameter["optimizer"],"RMSprop",[float(config.config["parameter"]["optimizer_lr"])]) #优化器也是返回了类但是不要对象
            self.m_model.compile(loss=self.m_loss,optimizer=self.m_optimizer,metrics=['accuracy'])
            self.train_num = parameter["train_generator"].samples//int(config.config["parameter"]["batch_size"])
            self.valid_num = parameter["valid_generator"].samples//int(config.config["parameter"]["batch_size"])
            self.model_path = os.path.join(parameter["new_model_path"],parameter["train_model_name"])
            self.result_path = os.path.join(self.model_path,"model_result")
            self.m_callbacks = self.mid_model_callback(self.model_path,self.result_path)
            self.m_model.fit_generator(
                parameter["train_generator"],
                steps_per_epoch=self.train_num,
                shuffle=True,
                epochs=int(parameter["iterate_times"]),
                validation_data=parameter["valid_generator"],
                validation_steps=self.valid_num,
                callbacks=self.m_callbacks
            )
            self.m_model.save("{}/all_{}.h5".format(parameter["model_fileaddr"],parameter["train_model_name"]))#
            return True,parameter
        except Exception as e:
            log.error("training error {}".format(e))
            return False,parameter
    def mid_model_init_train(self,parameter):
        if config.config["gpu_control"]["open"] == "1":
            try:
                self.memory_size = config.config["memory_size"]["mm_size"]
                self.gpu_init(self.memory_size)
            except Exception as e:
                log.error("gpu error {}".format(e))
        #数据增强器  配置文件
        self.train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=40, # 随机旋转角度的范围
                                width_shift_range=0.2, # 随机转换图片宽度的范围
                                height_shift_range=0.2, # 随机转换图片高度的范围
                                shear_range=0.2, # 随机剪切转换比例
                                zoom_range=0.2, # 随机放缩比例
                                horizontal_flip=True,# 开启水平翻转
                                fill_mode='nearest' # 填充策略
                                )
        self.valid_datagen = ImageDataGenerator(rescale=1./255)
        image_height, image_width = self.mid_height_width(parameter)#320x480 h_w
        self.model_path = os.path.join(parameter["new_model_path"],parameter["train_model_name"])
        self.result_path = os.path.join(self.model_path,"model_result")
        parameter.update({"model_fileaddr":self.result_path})
        dir_operator.create_model_save_dir(self.result_path)
        self.train_dataset = ""
        self.vaild_dataset = ""
         #获取训练集的图片增强生成器
        self.train_generator = train_datagen.flow_from_directory(
                self.train_dataset,
                target_size=(image_height, image_width),
                classes=parameter["target"].keys(),#数据库数据加载--》、
                batch_size=parameter["batch_size"],#--》配置文件
                shuffle=True,
                class_mode=config.config["parameter"]["class_mode"]) #写死
            #获取测试集的图片增强生成器        
        self.valid_generator = valid_datagen.flow_from_directory(
                self.vaild_dataset,
                target_size=(image_height, image_width),
                classes=parameter["target"].keys(),
                batch_size=int(config.config["parameter"]["batch_size"]),#每批次训练的大小
                shuffle=True,
                class_mode=config.config["parameter"]["class_mode"]) 
        data.update({"train_generator":self.train_generator,"valid_generator":self.valid_generator})

        self.mid_package_program(parameter)
        return True
    def mid_model_ass_train(self,data):
        # index_calculation(model_file_path,dataset_path)
        return True
    def mid_model_opt_train(self,data):
        # model_opti_train(model_file_path,new_model_path,dataset_path)
        return True

model_train = ModelTrain()


if __name__ == "__main__":
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
        "network_structure":"keras.applications.resnet50.ResNet50",#网络结构
        "optimizer":"keras.optimizers",#优化器
        "loss_value":"keras.losses",#损失值
        "callback":["1","2","3"],#回调函数
        "measure":["11","22","33"],#度量器
        #注意：评估不需要指定模型的存放地址，为None即可
        "new_model_path":"/home/liangxs/LXS_TESXT/ModelingSystem_Mid/ModelFile",#相对路径
        "train_dataset_id":[3,4,5],#训练数据集id
        "training_status":1, #训练状态
        "target" : {'jqf1qingwei': 0, 'jqf2qingdu': 1, 'jqf3zhongdu': 2, 'jqf4zhongdu': 3, 'jqf5yanzhong': 4}
    }
    # model_train.mid_height_width({"reslution":"320x480"})
    A = ModelTrain()
    # print(A.mid_model_init_train(queue_config))
    # print(A.mid_create_model(queue_config))
    print(A.mid_package_program(queue_config))
