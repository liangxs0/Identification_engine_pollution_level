from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json
from tensorflow import keras

from functools import reduce
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from PIL import Image
from pylab import *
from keras.callbacks import ReduceLROnPlateau
import math
import shutil
from scipy.ndimage import *
import cv2

from mid_ds_image_tool import *
from mid_ds_io import *

class DsError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class DataSet(object):    
    def __init__(self, dss=None, target=None, parent=None, name='sd'):
        self.dss = dss
        self.target = target
        self.parent = parent
        self.name = name

    @staticmethod
    def load(directory):
        dss, target = get_all_data(directory)
        dss = shuffle([item for sublist in dss for item in sublist])
        return DataSet(dss, target, None, 'sd')

    def is_grey(self):
        i = len(self.dss[0][1].shape)
        return len(self.dss[0][1].shape) is not 3

    def grey(self):
        res = [np.array(Image.fromarray(e[1]).convert('L')) for e in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0], u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'grey')

    def union(self, ds):
        if self.target != ds.target:
            raise DsError('dataset can not be union')
        dss = []
        dss.extend(ds.dss)
        dss.extend(self.dss)
        return DataSet(dss, self.target, self, 'union')

    def split(self, ratio):
        num = len(self.dss)  #数据集总条数（一张图像为一条数据）
        idx = np.array(range(0, num))
        np.random.shuffle(idx)
        self.dss = np.array(self.dss)[idx]
        train_indices = np.random.choice(num, round(num * ratio), replace=False)  
        test_indices = np.array(list(set(range(num)) - set(train_indices)))
        dss = self.dss 
        return DataSet(dss[train_indices].tolist(), self.target, self, 'split'), DataSet(dss[test_indices].tolist(), self.target, self, 'split')

    def epf_shift(self):
        res = [cv2.pyrMeanShiftFiltering(im[1], 10, 50) for im in self.dss]
        union = zip(res, self.dss)
        union = list(filter(lambda e: e[0] is not None, union))
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'epf_shift')
            
    def epf_bi(self):
        res = [cv2.bilateralFilter(im[1], 0, 100, 5) for im in self.dss]
        union = zip(res, self.dss)
        union = list(filter(lambda e: e[0] is not None, union))
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'epf_bi')
    
    def ed_sobel(self):
        res = [sobel(e[1]) for e in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'ed_sobel')

    def nr_gaussian(self):
        res = [cv2.GaussianBlur(e[1], (15,15), 0) for e in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'nc_gaussian')

    def nr_median(self):
        res = [cv2.medianBlur(e[1], 5) for e in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'nc_median')

    def nr_mean(self):
        res = [cv2.fastNlMeansDenoisingColored(im[1], None, 10, 10, 7, 21) for im in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'nc_mean')

    def hist(self):
        if self.is_grey():
            res = [histeq_grey(im[1]) for im in self.dss]
        else:
            res = [histeq_rgb(im[1]) for im in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'hist')


        


    def denoise(self, tolerance=0.1):
        if self.is_grey():
            res = [denoise_grey(im[1], im[1], tolerance) for im in self.dss]
        else:
            res = [denoise_rgb(im[1], im[1], tolerance) for im in self.dss]
        zdss = zip(res, self.dss)
        ndss = [(e[1][0], e[0][0].astype('uint8'), e[1][2]) for e in zdss]
        zdss = zip(res, self.dss)
        tdss = [(e[1][0], e[0][1].astype('uint8'), e[1][2]) for e in zdss]

        return DataSet(ndss, self.target, self, 'n_noise'), DataSet(tdss, self.target, self, 't_noise')

    def mean_denoise_color(self):
        if self.is_grey():
            res = [m_denoise_grey(e[1]) for e in self.dss]
        else:
            res = [m_denoise_color(e[1]) for e in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'm_denoise')



    def mean_denoise(self):
        res = [cv2.fastNlMeansDenoisingColored(im[1], None, 10, 10, 7, 21) for im in self.dss]
        union = zip(res, self.dss)
        newDss = [(u[1][0], u[0].astype('uint8'), u[1][2]) for u in union]
        return DataSet(newDss, self.target, self, 'cv2_mean')

    

    def predict(self, model, target):
        input_shape = model.inputs[0].shape

        image_width = input_shape[1]
        image_height = input_shape[2]
        t1 = [Image.fromarray(img[1]) for img in self.dss]
        t2 = [np.asarray(e.resize((image_height, image_width))) for e in t1]
        t3 = np.array(t2)
        t4 = t3 / 255.
        #tmp = np.array([Image.fromarray(img[1]).resize((image_height, image_width)) for img in self.dss]) / 255.
        #tmp = np.array([Image.fromarray(im[1].astype('uint8')).resize([image_height, image_width])/255. for im in self.dss])

        y_pred = tf.argmax(model.predict(t4), axis=1).numpy()
        target_ver = {v : k for k, v in target.items()}

        newDss = [(img[0], img[1], target_ver[y_pred[idx]]) for idx, img in enumerate(self.dss)]
        return DataSet(newDss, self.target, self, 'predict')
        
    def get_tp_fp(self):
        '''计算混淆矩阵，行为人工分类，列为计算分类
        '''
        #dss_1 = [0, 0, 0, 1, 3, 2, 3, 4, 2]
        dss = list(zip(self.parent.dss, self.dss))
        fp_tp = [[len(list(
            filter(lambda x: x[1][2] == ie, list(filter(lambda x: x[0][2] == e, dss)))
            )) for ie in self.target.keys()] for e in self.target.keys()]
        fp_tp = [[0, row[0], row[1], row[2], row[3], row[4], 0] for row in fp_tp]
        fp_tp.insert(0, [0, 0, 0, 0, 0, 0, 0])
        fp_tp.append([0, 0, 0, 0, 0, 0, 0])
        return fp_tp



    def accuracy(self):
        tp_fp_matrix = self.get_tp_fp()
        res = list(reduce(lambda s, e: (s[0] + tf.reduce_sum(e), s[1] + e[s[2]], s[2] + 1), tp_fp_matrix, (0, 0, 0)))
        return {'accuracy': round(float(res[1]) / float(res[0]), 3)}

    def fuzzy_accuracy(self):
        tp_fp_matrix = self.get_tp_fp()
        total = 0
        acc_num = 0
        for i, row in enumerate(tp_fp_matrix):
            if i > 0 and i < 6:
                total = total + tf.reduce_sum(row)
                acc_num = acc_num + row[i] + row[i-1] + row[i+1]
        return {'fuzzy_accuracy': round(float(acc_num) / float(total), 3)}

    def fuzzy_upper_accuracy(self):
        tp_fp_matrix = self.get_tp_fp()
        total = 0
        acc_num = 0
        for i, row in enumerate(tp_fp_matrix):
            if i > 0 and i < 6:
                total = total + tf.reduce_sum(row)
                acc_num = acc_num + row[i]  + row[i+1]
        return {'fuzzy_upper_accuracy': float(acc_num) / float(total)}


    def recall(self):
        tp_fp_matrix = self.get_tp_fp()
        target_ver = {v : k for k, v in self.target.items()}
        res = {target_ver[i-1]: np.round((tf.cast(t[i], tf.float32) / tf.cast(tf.reduce_sum(t), tf.float32)).numpy(), 3) for i, t in enumerate(tp_fp_matrix) if i > 0 and i < 6}       
        avg = np.round(tf.reduce_mean(list(res.values())).numpy(), 3)
        return {'avg_recall': avg, 'info' : res}

    def fuzzy_recall(self):
        tp_fp_matrix = self.get_tp_fp()
        target_ver = {v : k for k, v in self.target.items()}
        res = {target_ver[i-1]: np.round((tf.cast((t[i-1]+t[i]+t[i+1]), tf.float32) / tf.cast(tf.reduce_sum(t), tf.float32)).numpy(), 3) for i, t in enumerate(tp_fp_matrix) if i > 0 and i < 6}       
        avg = np.round(tf.reduce_mean(list(res.values())).numpy(), 3)
        return {'avg_fuzzy_recall': avg, 'info' : res}

    def precision(self):
        tp_fp_matrix = self.get_tp_fp()
        tp_fp_matrix = np.transpose(np.array(tp_fp_matrix))
        target_ver = {v : k for k, v in self.target.items()}
        res = {target_ver[i-1]: np.round((tf.cast(t[i], tf.float32) / tf.cast(tf.reduce_sum(t), tf.float32)).numpy(), 3) for i, t in enumerate(tp_fp_matrix) if i > 0 and i < 6}
        avg = np.round(tf.reduce_mean(list(res.values())).numpy(), 3)
        return {'avg_precision': avg, 'info' : res}


    def fuzzy_precision(self):
        tp_fp_matrix = self.get_tp_fp()
        tp_fp_matrix = np.transpose(np.array(tp_fp_matrix))
        target_ver = {v : k for k, v in self.target.items()}
        res = {target_ver[i-1]: np.round((tf.cast((t[i-1]+t[i]+t[i+1]), tf.float32) / tf.cast(tf.reduce_sum(t), tf.float32)).numpy(), 3) for i, t in enumerate(tp_fp_matrix) if i > 0 and i < 6}
        avg = np.round(tf.reduce_mean(list(res.values())).numpy(), 3)
        return {'avg_fuzzy_precision': avg, 'info' : res}

    def f1_score(self):
        z = list(zip(self.precision()['info'].values(), self.recall()['info'].values()))  
        target_ver = {v : k for k, v in self.target.items()}
        s = {target_ver[i] : np.round((2.0 * p * r)/(p + r), 3) for i, (p, r) in enumerate(z)}
        tmp = s.values()
        return {'f1_score': np.round(tf.reduce_mean(list(s.values())).numpy(), 3), 'info' : s}

    def fuzzy_f1_score(self):
        z = list(zip(self.fuzzy_precision()['info'].values(), self.fuzzy_recall()['info'].values()))  
        target_ver = {v : k for k, v in self.target.items()}
        s = {target_ver[i] : np.round((2.0 * p * r)/(p + r), 3) for i, (p, r) in enumerate(z)}
        tmp = s.values()
        return {'fuzzy_f1_score': np.round(tf.reduce_mean(list(s.values())).numpy(), 2), 'info' : s}

    def g_score(self):
        z = list(zip(self.precision()['info'].values(), self.recall()['info'].values()))  
        target_ver = {v : k for k, v in self.target.items()}
        s = {target_ver[i] : np.round(math.sqrt(p*r), 3) for i, (p, r) in enumerate(z)}
        return {'g_score' : np.round(tf.reduce_mean(list(s.values())).numpy(), 3), 'info' : s}

    def fuzzy_g_score(self):
        z = list(zip(self.fuzzy_precision()['info'].values(), self.fuzzy_recall()['info'].values()))  
        target_ver = {v : k for k, v in self.target.items()}
        s = {target_ver[i] : np.round(math.sqrt(p*r), 3) for i, (p, r) in enumerate(z)}
        return {'fuzzy_g_score' : np.round(tf.reduce_mean(list(s.values())).numpy(), 3), 'info' : s}
        
    def summary(self):
        '''
        汇总所有的评价指标
        '''
        return {'accuracy': self.accuracy(),
                'precision': self.precision(), 
                'recall': self.recall(),
                'f1_score': self.f1_score(), 
                'g_score': self.g_score()}


    def fuzzy_summary(self):
        '''
        汇总所有的评价指标
        '''
        return {
                'fuzzy_accuracy': self.fuzzy_accuracy(), 
                'fuzzy_precision': self.fuzzy_precision(),
                'fuzzy_recall': self.fuzzy_recall(), 
                'fuzzy_f1_score': self.fuzzy_f1_score(),
                'fuzzy_g_score': self.fuzzy_g_score()}

    def plot(self, path):
        labels = ['qw', 'qd', 'zd', 'zzd', 'yz']
        p = self.precision()
        f_p = self.fuzzy_precision()
        plt.subplot(221)
        plot_s(plt, 
            labels, 
            list(p['info'].values()), 
            list(f_p['info'].values()), 
            'precision')
        plt.subplot(222)

        p = self.recall()
        f_p = self.fuzzy_recall()
        plot_s(plt, 
            labels, 
            list(p['info'].values()), 
            list(f_p['info'].values()), 
            'recall')
        plt.subplot(223)

        p = self.f1_score()
        f_p = self.fuzzy_f1_score()
        plot_s(plt, 
            labels, 
            list(p['info'].values()), 
            list(f_p['info'].values()), 
            'f1_score')
        plt.subplot(224)

        p = self.g_score()
        f_p = self.fuzzy_g_score()
        plot_s(plt, 
            labels, 
            list(p['info'].values()), 
            list(f_p['info'].values()), 
            'g_score')
        
        plt.savefig(path)

    def save(self, directory_path):
        if  os.path.exists(directory_path): shutil.rmtree(directory_path)
        os.makedirs(directory_path)

        for k, _ in self.target.items():
            os.makedirs(os.path.join(directory_path, k))

        for e in self.dss:
            file_name = os.path.splitext(os.path.basename(e[0]))[0] + '.JPG'
            image_file = os.path.join(os.path.join(directory_path, e[2]), file_name)#os.path.splitext(os.path.basename(e[0]))[0] + '.JPG')
            #image = Image.fromarray(e[1].astype('uint8'))
            try:
                Image.fromarray(e[1]).save(image_file)
            except Exception as e:
                print(e, image_file)

        with open(os.path.join(directory_path, 'readme.txt'), 'a') as f:
            t = self
            while t is not None:
                f.write(t.name + '\n')
                t = t.parent

 
if __name__ == "__main__":
    a = DataSet()
    
