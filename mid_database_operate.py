# coding: utf-8
'''
describe:数据库有关操作
author:lxs
version:v3
date:2020
'''
from mid_database_models import *
from mid_config_operator import config
from mid_log_set import log
from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker
import time

Tables = {
    "dataset_info":DatasetsDatasetsinfo,
    "dataset_test_model":ModelmanagementDatasettestmodel,
    "dataset_train_model":ModelmanagementDatasettrainingmodel,
    "dataset_test_err":ModelmanagementTestlabelerror,
    "dataset_test_index":ModelmanagementTestlabelindex,
    "dataset_train_index":ModelmanagementTraininglabelindex,
    "dataset_model_info":ModelmanagementTrainingmodelinfo,#训练模型信息
}

class DatabaseOpetor(object):
    def __init__(self):
        # 创建的数据库引擎
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(config.config["db1"]["db_user"],config.config["db1"]["db_psk"],
                                            config.config["db1"]["db_host"],config.config["db1"]["db_port"],
                                            config.config["db1"]["db_name"]),pool_recycle=3600)
        self.DBSession = sessionmaker(bind=self.engine)#创建session类型

    def dataset_info_get(self,dataset_ids):
        data = []
        self.session = self.DBSession()
        for id in dataset_ids:
            try:
                data.append(self.session.query(Tables["dataset_info"]).get(id))
            except Exception as e:
                log.error("The dataset query failed {}".format(e))
                return False
        self.session.close()
        return {id:name.dataset_name for id,name in zip(dataset_ids,data)}
    def model_info_get(self,model_id,model_version):
        self.session = self.DBSession()
        now_mdoel_info = self.session.query(Tables["dataset_model_info"]).get(model_id)
        if now_mdoel_info.model_status is 1:
            last_version = None
        if model_version is None:
            try:
                last_version = self.session.query(Tables["dataset_train_model"]).filter_by(training_model_id=model_id).order_by(Tables["dataset_train_model"].id).all()#
                if len(last_version) is 0:
                    last_version = None
                else:
                    last_version = last_version[len(last_version)-1]
                n_version_info = None
                self.session.close()
            
                return now_mdoel_info,n_version_info,last_version
            except Exception as e:
                self.session.close()
                log.error("{} model:{} info get error".format(e,model_id))
                return False
        else:
            try:
                last_version = self.session.query(Tables["dataset_train_model"]).filter_by(training_model_id=model_id).order_by(Tables["dataset_train_model"].id).all()#
                n_version_info = self.session.query(Tables["dataset_train_model"]).filter_by(training_model_id=model_id,model_version=model_version).all()
                self.session.close()
                return now_mdoel_info,n_version_info[0],last_version[len(last_version)-1] #name,address,last_version
            except Exception as e:
                log.error("{} model:{} info get error".format(e,model_id))
                self.session.close()
                return False
    def test_model_info_get(self,test_model_id,session):
        try:
            test_model_info = session.query(Tables["dataset_test_model"]).filter_by(testing_model_id=test_model_id).all()
            return test_model_info[len(test_model_info)-1]
        except Exception as e:
            log.error("test 0model info get fail {}".format(e))
            return False
    def updata_train_mdoel_status(self,model_id,status):
        self.session = self.DBSession()
        try:
            model_info = self.session.query(Tables["dataset_model_info"]).filter_by(id = model_id).all()
            model_info[0].training_status = status
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            log.error("model:{} status change failed{}".format(model_id,e))
            self.session.close()
            return False
    def insert_init_opt_result_save(self,data):
        # try:
        #     n_traininginfo_id = self.model_info_get(data["training_model_id"],None)[2].id
        # except Exception as e:
        #     log.error("model info get error {}".format(e))
        #     return False
        self.session = self.DBSession()
        insert_data = Tables["dataset_train_model"](
            training_time = data["training_time"],
            accuracy_rate = data["accuracy_rate"],
            model_version = data["model_version"],
            model_fileaddr = data["model_fileaddr"],
            dataset_list = data["dataset_list"],
            training_model_id = data["training_model_id"]
            )
        try:
            self.session.add(insert_data)
            self.session.commit()
            
            try:
                n_traininginfo_id = self.model_info_get(data["training_model_id"],None)[2].id
            except Exception as e:
                log.error("model info get error {}".format(e))
                return False
            for da in data["tags_index"]:
                insert_da = Tables["dataset_train_index"](
                    F1score = da["F1score"],
                    Gscore = da["Gscore"],
                    precision_rate = da["precision_rate"],
                    recall_rate = da["recall_rate"],
                    label_id = da["label_id"],
                    traininginfo_id = n_traininginfo_id
                )
                self.session.add(insert_da)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            log.error("data insert error {}".format(e))
            self.session.close()
            return False
    def insert_ass_result_save(self,data):
        n_traininginfo_id = self.model_info_get(data["training_model_id"],data["model_version"])[1].id

        self.session = self.DBSession()
        insert_data = Tables["dataset_test_model"](
            test_time = data["training_time"],
            accuracy_rate = data["accuracy_rate"],
            dataset_list = data["dataset_list"],
            testing_model_id = n_traininginfo_id
        )
        try:
            self.session.add(insert_data)
            self.session.commit()
        except Exception as e:
            log.error("test data insertion failed {}".format(e))
            self.session.close()
            return False
        try:
            n_test_mode_id = self.test_model_info_get(n_traininginfo_id,self.session).id
            for da in data["tags_index"]:
                insert_da = Tables["dataset_test_index"](
                    F1score = da["F1score"],
                    Gscore = da["Gscore"],
                    precision_rate = da["precision_rate"],
                    recall_rate = da["recall_rate"],
                    label_id = da["label_id"],
                    testinfo_id = n_test_mode_id
                )
                self.session.add(insert_da)
            self.session.commit()
        except Exception as e:
            log.error("test data index insertion failed {}".format(e))
            self.session.close()
            return False
        try:
            for da_img in data["error_images"]:
                insert_da_img = Tables["dataset_test_err"](
                    pic_address = da_img["pic_address"],
                    old_label = da_img["old_label"],
                    new_label = da_img["new_label"],
                    testinfo_id = n_test_mode_id
                )
                self.session.add(insert_da_img)
            self.session.commit()
        except Exception as e:
            log.error("error picture recording failed {}".format(e))
            self.session.close()
            return False
        self.session.close()
        return True


dbase = DatabaseOpetor()

if __name__ == "__main__":
    DD = DatabaseOpetor()
    # print(DD.dataset_info_get([1,2]))
    print(DD.model_info_get(2,"V1")[2].model_version)
    # DD.updata_train_mdoel_status(78,10)
    #测试数据
    data = {
        "training_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "accuracy_rate":90.0,
        "model_version":"V14",
        "model_fileaddr":"http:/*?/",
        "dataset_list":"1,2,3",
        "training_model_id":73,
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

    # print(DD.insert_init_result_save(data))
    # print(DD.insert_ass_result_save(data))