import numpy as np
from PIL import Image
import os

# 对数据集洗牌（随机打乱，为随机抽样）
def shuffle(dataset):
    '''数据集洗牌
    dataset: 数据对象的列表列表
    返回： 
    '''
    idx = np.array(range(0, len(dataset)))
    np.random.shuffle(idx)
    dataset = np.array(dataset)[idx]
    return dataset.tolist()


def read_image(image_path):
    '''
    从指定的文件中装入图像
    返回：（路径，图像）的元组
    '''
    try:
        img = Image.open(image_path)#.resize((640, 480))
        if img.mode is not 'RGB':
            print(image_path, img.mode)
            return (image_path, None)
        else:
            image = np.array(Image.open(image_path), 'uint8')
            return  (image_path, image)
        # image = np.array(Image.open(image_path), 'uint8')
        # pil_im = Image.fromarray(uint8(im))
        # image = np.array(pil_im.resize((576, 768)), 'uint8')
    except Exception as e:
        print("error image: ", image_path, e)
    return (image_path, None)



def get_image_set(subDir):
    '''
    从指定目录subDir下装载所有图像
    返回：(路径，图像，类别)的列表
    '''
    image_files = list(filter(lambda e: not e.startswith('.'), os.listdir(subDir)))
    subDs = [(read_image(os.path.join(subDir, file)), os.path.basename(subDir)) for file in image_files if len(image_files) > 0]
    subDs = list(map(lambda e: (e[0][0], e[0][1], e[1]), filter(lambda e: e[0][1] is not None, subDs)))
    return subDs



def get_all_data(directory):
    subDirs = os.listdir(directory)
    subDirs = list(filter(
        lambda x: (not x.startswith(('.'))) and (not x.endswith('.zip') and (not x == 'readme.txt')),
        subDirs
    ))
    subDirs.sort()
    ds = [get_image_set(os.path.join(directory, subDir)) for subDir in subDirs if len(subDirs) > 0]
    target = {e:i for i,e in enumerate(subDirs)}
    return ds, target

def insert(l, e):
    l.insert(0, e)
    return l

def normal(x_train):
    return x_train.astype('float32') / 255.

