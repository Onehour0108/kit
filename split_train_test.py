#将南方医的数据分成训练集和验证集两部分
import sys
import numpy as np   
import csv
from utils.utils import *
import utils.handle_huge_img as hbi
import cv2   
import Config
import pandas as pd
import math
import gc
import os    
import sys
import random
# import seg_dense_random as sdr
dir = '../Pathology'
save_dir = '../'

SIZE_PATCH_20X = 20000
REVOLUTION = "20X"
DATA_CENTER = "nanfang" #"nanfang" or "TCGA"

def return_nanfang_uesfull_patients(conf):
    df=pd.read_csv(conf.extract_label_path["nanfang"], encoding="GBK") 
    info("The dataframe has {} row and {} column".format(df.shape[0], df.shape[1]))
    usefull_data = []
    record_id = {}
    mz = MyZip(df['免疫组化结果'].values,df['住院号/ID'].values,np.arange(len(df['免疫组化结果'])))
    idh_flag = "idh"
    for i, j, num in mz:
        _str = i[0].lower()
        id = j[0]
        if _str.find(idh_flag)>=0:
            if record_id.get(id) != None:
                continue
            record_id[id] = 1
            # sp = _str.split(idh_flag)
            # idh_stage = sp[1][0]
            usefull_data.append(df.iloc[num].values[0])
    usefull_dataframe = pd.core.frame.DataFrame(usefull_data)
    usefull_dataframe.columns = df.columns.values
    info("The return dataframe has {} row and {} column".\
                format(usefull_dataframe.shape[0], usefull_dataframe.shape[1]))
    return usefull_dataframe

def return_TCGA_usefull_patients(conf):
    df=pd.read_csv(conf.extract_label_path["TCGA"]) 
    info("The dataframe has {} row and {} column".format(df.shape[0], df.shape[1]))
    usefull_data = []
    # print(df["Case"])
    # print(df.columns.values)
    # print(df.iloc[0].values)
    # print(df['诊断切片DX'].values)
    mz = MyZip(df['诊断切片DX'].values, df['IDH status'].values,np.arange(len(df['诊断切片DX'])))
    for i, j, num in mz:
        if math.isnan(i[0]) or isinstance(j[0], float) :
            continue
        usefull_data.append(df.iloc[num].values[0])
    usefull_dataframe = pd.core.frame.DataFrame(usefull_data)
    usefull_dataframe.columns = df.columns.values
    info("The return dataframe has {} row and {} column".\
                format(usefull_dataframe.shape[0], usefull_dataframe.shape[1]))
    return usefull_dataframe


USED_PATIENT_FUN    = {"nanfang"    : return_nanfang_uesfull_patients,
                        "TCGA"      : return_TCGA_usefull_patients}


conf = Config.config()
random.seed(conf.seed)
label_path = conf.label_of_train_test

just_ff(label_path, create_floder=True)
show_config(label_path,param = locals())

usefull_dataframe = USED_PATIENT_FUN[DATA_CENTER](conf)
rate = conf.train_rate_nanfang
cutoff = len(usefull_dataframe['免疫组化结果']) * rate
mz = MyZip(usefull_dataframe['免疫组化结果'].values,np.arange(len(usefull_dataframe['免疫组化结果'])))

idh_flag = "idh"
train_data  = []
text_data = []

train_idh = 0
train_no_idh = 0
test_idh = 0
test_no_idh = 0
for i,  num in mz:
    _str = i[0].lower()
    _b = _str.split(idh_flag)[1]
    _b = _b[0:7]
    i = random.randint(1,10)
    if i % 10 > int(rate * 10):
        
        # print(_b)
        if _b.find("+")>=0:
            test_idh+=1
        elif _b.find("-")>=0 or  _b.find("弱")>=0:
            test_no_idh +=1
        else:
            # print(_b)
            print(_b,usefull_dataframe.iloc[num].values[0][1])
        text_data.append(usefull_dataframe.iloc[num].values[0])

    else:
        if _b.find("+")>=0:
            train_idh+=1
        elif _b.find("-")>=0 or  _b.find("弱")>=0:
            train_no_idh +=1
        else:
            # print(_b)
            print(_b,usefull_dataframe.iloc[num].values[0][1])
        train_data.append(usefull_dataframe.iloc[num].values[0])
info(train_idh,train_no_idh,test_idh,test_no_idh)
info(np.sum([train_idh,train_no_idh,test_idh,test_no_idh]))
new_usefull_dataframe = pd.core.frame.DataFrame(train_data)
new_usefull_dataframe.columns = usefull_dataframe.columns.values
# usefull_dataframe = pd.DataFrame(usefull_dataframe)
new_usefull_dataframe.to_csv(os.path.join(conf.label_of_train_test,"train.csv"))
new_usefull_dataframe = pd.core.frame.DataFrame(text_data)
new_usefull_dataframe.columns = usefull_dataframe.columns.values
# usefull_dataframe = pd.DataFrame(usefull_dataframe)
new_usefull_dataframe.to_csv(os.path.join(conf.label_of_train_test,"test.csv"))