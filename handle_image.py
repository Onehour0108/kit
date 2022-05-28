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
import utils.handle_img as hi
import sys
# import seg_dense_random as sdr
dir = '../Pathology'
save_dir = '../'
COMPRESS_PARAMS = [cv2.IMWRITE_JPEG_QUALITY, 80]
# cv2.imwrite('1.png', img, COMPRESS_PARAMS)
SIZE_BIG_PATCH = 24*256
REVOLUTION = "40X"
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

def get_TCGA_svs_path(svs_path,floder,num, use_full_patients):
    image_floder = os.path.join(svs_path,floder)
    if not just_ff(image_floder):
        err("The floder '{}' donet exist!!".format(image_floder))

    files           = os.listdir(image_floder)
    if len(files)   <=0 :
        err("The patient '{}' has zero section!!".format(floder))
    for f in files:
        if f.find(".svs")>0:
            return os.path.join(image_floder, f)
    err("Donot find .svs file in patient '{}'!!".format(floder))


def get_nanfang_svs_path(svs_path,floder,num, use_full_patients):
    ignore_warning()
    
    pathology_id = use_full_patients["病理检查号"].values[num]
    image_floder = os.path.join(svs_path,floder,pathology_id)
    # show_config(pathology_id, image_floder,param= locals())
    if not just_ff(image_floder):
        warn("The floder '{}' donot exist!!".format(image_floder))
        return ''

    files   = os.listdir(image_floder)
    if len(files)   <=0 :
        err("The patient '{}' has zero section!!".format(floder))

    for f in files:
        id_, suffix = os.path.splitext(f)
        if suffix != ".txt": continue
        if id_.find("0")>=0:
            return ''
        else:
            for i in files:
                _, suffix = os.path.splitext(i)
                # print(id_,suffix)
                if i[0]=="." or suffix != '.svs': 
                    continue
                index_ = i.split("_")[-1]
                
                if index_.find(id_)>=0:
                    ret_path = os.path.join(image_floder, i) 
                    if not just_ff(ret_path, file = True):
                        err("{} is not exist!".format(ret_path))
                    return ret_path
            err("{} .txt file is error!!".format(image_floder))

    for f in files:
        id_, suffix = os.path.splitext(f)
        if suffix == ".xml":
            return os.path.join(image_floder, id_+".svs")
    for f in files:
        if f[0] == '.':
            continue
        if image_floder.find('000124754')>=0:
            break
        #有栅栏状,删掉
        if image_floder.find('000033173')>=0:
            break
        #脱色了，删掉
        if image_floder.find('000005893')>=0:
            break
        if f.find(".svs")>0:
            #这个文件读不出来
            if image_floder.find('PA1726225')>=0 and f.find('001.svs')>=0:
                continue
            if image_floder.find("PA1625590")>=0 and f.find('1625590_2')>=0:
                continue
            #这个svs文件格式错误，读不出来
            if image_floder.find("PA1822043")>=0 and f.find('1822043_001')>=0:
                continue
            return os.path.join(image_floder, f)
    warn("Donot find .svs file in patient '{}'!!".format(floder))
    return ''
USED_PATIENT_FUN    = {"nanfang"    : return_nanfang_uesfull_patients,
                        "TCGA"      : return_TCGA_usefull_patients}

GET_SVS_PATH        = {"nanfang"    : get_nanfang_svs_path,
                        "TCGA"      : get_TCGA_svs_path}

def just_svs_patches(files,id):
    # print(files,id)
    for f in files:
        if f.find(id)>=0:
            return True
    return False

def handle_img(conf):
    svs_path = conf.svs_path[DATA_CENTER]
    big_patch_save_path = conf.big_patch_save_path[REVOLUTION][DATA_CENTER]

    # just_ff(big_patch_save_path, create_floder=True)
    show_config(svs_path,big_patch_save_path,param = locals())

    # patches = os.listdir(big_patch_save_path)
    usefull_dataframe = USED_PATIENT_FUN[DATA_CENTER](conf)
    for num, floder in enumerate(usefull_dataframe[conf.patient_id_cloumn[DATA_CENTER]].values):
        # if floder.find("000050713")<0:continue
        file_path   = GET_SVS_PATH[DATA_CENTER](svs_path,floder,num, usefull_dataframe)

        if file_path=='':
            warn("{} can not find .svs image. Continue!!".format(floder))
            continue
        # print('*******',os.path.join(big_patch_save_path,floder))
        save_path_10X   = os.path.join(conf.big_patch_save_path["10X"][DATA_CENTER], floder)
        save_path_20X   = os.path.join(conf.big_patch_save_path["20X"][DATA_CENTER], floder)
        save_path_40X   = os.path.join(conf.big_patch_save_path["40X"][DATA_CENTER], floder)
        # info(save_path_10X,save_path_20X)
        if  just_ff(save_path_10X, info=False) and \
                just_ff(save_path_20X, info=False)and \
                just_ff(save_path_40X, info=False)    : 
            tips("Patient '{}' has been extract! Contine!".format(floder))
            continue

        info("{}".format(file_path))
        # continue
        flow("The {} of the {}".format(num, usefull_dataframe.shape[0]))

        def handle_patch(patch, patch_index,h):
            just_ff(save_path_40X, create_floder=True)
            hi.cv2_writer(os.path.join(save_path_40X,floder+'-{}-{}-{}-{}.jpg'.\
                            format(patch_index[0],patch_index[1],\
                                patch_index[2],patch_index[3])),
                            patch, COMPRESS_PARAMS)

            just_ff(save_path_20X, create_floder=True)
            patch = cv2.resize(patch, (patch.shape[1]//2, patch.shape[0]//2))
            patch_index = [i//2 for i in patch_index]
            hi.cv2_writer(os.path.join(save_path_20X,floder+'-{}-{}-{}-{}.jpg'.\
                            format(patch_index[0],patch_index[1],\
                                patch_index[2],patch_index[3])),
                            patch, COMPRESS_PARAMS)

            just_ff(save_path_10X, create_floder=True)
            patch = cv2.resize(patch, (patch.shape[1]//2, patch.shape[0]//2))
            patch_index = [i//2 for i in patch_index]
            hi.cv2_writer(os.path.join(save_path_10X,floder+'-{}-{}-{}-{}.jpg'.\
                            format(patch_index[0],patch_index[1],\
                                patch_index[2],patch_index[3])),
                            patch, COMPRESS_PARAMS)

        hbi.get_WSI_image_of_level(file_path, scale = conf.down_sample_rate[REVOLUTION],\
            small_size=SIZE_BIG_PATCH, handle_level=1, handle_fun=handle_patch, return_img=False)

        # del img
        # gc.collect()

if __name__ == '__main__':
    conf = Config.config()
    # for key in conf.WSI_info.keys():
    handle_img(conf) 
    
# if not just_ff(save_path_40X, info=False):
#     just_ff(save_path_40X, create_floder=True)
#     img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))

#     index   = hbi.gen_patches_index(img.shape[:2], img_size=SIZE_BIG_PATCH,stride=SIZE_BIG_PATCH,\
#                         keep_last_size=False)
#     for ind in index:
#         hi.cv2_writer(os.path.join(save_path_40X,floder+'-{}-{}-{}-{}.jpg'.\
#                     format(ind[0],ind[1],ind[2],ind[3])),
#                     img[ind[0]:ind[1], ind[2]:ind[3], :], COMPRESS_PARAMS)


    
