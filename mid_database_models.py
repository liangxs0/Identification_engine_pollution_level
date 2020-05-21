# coding: utf-8
from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


# class DatasetsDatasetsclassify(Base):
#     __tablename__ = 'datasets_datasetsclassify'

#     id = Column(INTEGER(11), primary_key=True)
#     classify_name = Column(String(255), nullable=False)
#     classify_time = Column(DATETIME(fsp=6), nullable=False)
#     classify_quantity = Column(INTEGER(11), nullable=False)
#     dataset_id = Column(INTEGER(11), nullable=False)


class DatasetsDatasetsinfo(Base):
    __tablename__ = 'datasets_datasetsinfo'

    id = Column(INTEGER(11), primary_key=True)
    dataset_name = Column(String(255), nullable=False)
    dataset_time = Column(DATETIME(fsp=6), nullable=False)
    dataset_status = Column(INTEGER(11), nullable=False)
    dataset_fileaddr = Column(String(255))
    dataset_ratio = Column(String(255), nullable=False)
    dataset_describe = Column(String(255), nullable=False)
    dataset_part_id = Column(INTEGER(11), nullable=False)


# class DatasetsPartinfo(Base):
#     __tablename__ = 'datasets_partinfo'

#     id = Column(INTEGER(11), primary_key=True)
#     part_name = Column(String(255), nullable=False)


class ModelmanagementDatasettestmodel(Base):
    __tablename__ = 'modelmanagement_datasettestmodel'

    id = Column(INTEGER(11), primary_key=True)
    test_time = Column(DATETIME(fsp=6), nullable=False)
    accuracy_rate = Column(Float(asdecimal=True), nullable=False)
    dataset_list = Column(String(255), nullable=False)
    testing_model_id = Column(INTEGER(11), nullable=False)


class ModelmanagementDatasettrainingmodel(Base):
    __tablename__ = 'modelmanagement_datasettrainingmodel'

    id = Column(INTEGER(11), primary_key=True)
    training_time = Column(DATETIME(fsp=6), nullable=False)
    accuracy_rate = Column(Float(asdecimal=True), nullable=False)
    model_version = Column(String(255), nullable=False)
    model_fileaddr = Column(String(255), nullable=False)
    dataset_list = Column(String(255), nullable=False)
    training_model_id = Column(INTEGER(11), nullable=False)


# class ModelmanagementLabelinfo(Base):
#     __tablename__ = 'modelmanagement_labelinfo'

#     id = Column(INTEGER(11), primary_key=True)
#     label_time = Column(DATETIME(fsp=6), nullable=False)
#     label_name = Column(String(255), nullable=False)
#     label_describe = Column(String(255), nullable=False)


# class ModelmanagementReleaselabelindex(Base):
#     __tablename__ = 'modelmanagement_releaselabelindex'

#     id = Column(INTEGER(11), primary_key=True)
#     F1score = Column(Float(asdecimal=True), nullable=False)
#     Gscore = Column(Float(asdecimal=True), nullable=False)
#     precision_rate = Column(Float(asdecimal=True), nullable=False)
#     recall_rate = Column(Float(asdecimal=True), nullable=False)
#     label_id = Column(INTEGER(11), nullable=False)
#     release_model_id = Column(INTEGER(11), nullable=False)


# class ModelmanagementReleasemodel(Base):
#     __tablename__ = 'modelmanagement_releasemodel'

#     id = Column(INTEGER(11), primary_key=True)
#     model_name = Column(String(255), nullable=False)
#     model_time = Column(DATETIME(fsp=6), nullable=False)
#     model_part = Column(String(255), nullable=False)
#     model_fileaddr = Column(String(255), nullable=False)
#     accuracy_rate = Column(Float(asdecimal=True), nullable=False)
#     model_describe = Column(String(255), nullable=False)
#     user_id = Column(INTEGER(11), nullable=False)
#     user_name = Column(String(255), nullable=False)


class ModelmanagementTestlabelerror(Base):
    __tablename__ = 'modelmanagement_testlabelerror'

    id = Column(INTEGER(11), primary_key=True)
    pic_address = Column(String(255), nullable=False)
    old_label = Column(String(255), nullable=False)
    new_label = Column(String(255), nullable=False)
    testinfo_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTestlabelindex(Base):
    __tablename__ = 'modelmanagement_testlabelindex'

    id = Column(INTEGER(11), primary_key=True)
    F1score = Column(Float(asdecimal=True), nullable=False)
    Gscore = Column(Float(asdecimal=True), nullable=False)
    precision_rate = Column(Float(asdecimal=True), nullable=False)
    recall_rate = Column(Float(asdecimal=True), nullable=False)
    label_id = Column(INTEGER(11), nullable=False)
    testinfo_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTraininglabelindex(Base):
    __tablename__ = 'modelmanagement_traininglabelindex'

    id = Column(INTEGER(11), primary_key=True)
    F1score = Column(Float(asdecimal=True), nullable=False)
    Gscore = Column(Float(asdecimal=True), nullable=False)
    precision_rate = Column(Float(asdecimal=True), nullable=False)
    recall_rate = Column(Float(asdecimal=True), nullable=False)
    label_id = Column(INTEGER(11), nullable=False)
    traininginfo_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTrainingmodelinfo(Base):
    __tablename__ = 'modelmanagement_trainingmodelinfo'

    id = Column(INTEGER(11), primary_key=True)
    model_name = Column(String(255), nullable=False)
    model_time = Column(DATETIME(fsp=6), nullable=False)
    model_status = Column(INTEGER(11), nullable=False)
    accuracy_rate = Column(Float(asdecimal=True))
    model_describe = Column(String(255), nullable=False)
    user_id = Column(INTEGER(11))
    user_name = Column(String(255))
    model_part_id = Column(INTEGER(11), nullable=False)
    training_status = Column(INTEGER(11), nullable=False)
    release_version = Column(String(255), nullable=False)

