from posixpath import basename
import cv2
import sys
import random
import os
import glob
import numpy as np
import openslide  
from utils import handle_img as hi
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image

def reconstruct_wsi(files_floder):
    """
        将小块的patch重组成完整的patch，patch的格式为：
    """
wsi_path = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/ljc_test/img_10x/'
tile_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/ljc_test/tiles_overlay'
output_wsi_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/ljc_test/output_wsi/'
# get the list of all wsis
wsi_list = glob.glob(wsi_path + '*')
i=0
# get a random wsi from the list
# rand_wsi = np.random.randint(0,len(wsi_list))
for range_wsi in range(len(wsi_list)):
    wsi_file = wsi_list[range_wsi]
    wsi_ext = '.tif'
    wsi_basename = os.path.basename(wsi_file)
    wsi_basename = wsi_basename[:-(len(wsi_ext))]


    slide = openslide.open_slide(wsi_file)
    [w,h]=slide.level_dimensions[0]

    highth =1600
    width=1600

    ret  = np.zeros([h,w,3],dtype = np.uint8)

    i=i+1

    File_Path = tile_path+'/'+str(i)+'/'

    for x in tqdm(range(0,w,width)):
        if x+width > w:
        
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    img = hi.cv2_reader(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:h, x:w] = img
                else:
                    img = hi.cv2_reader(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:y+highth, x:w] = img
        else:
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    img = hi.cv2_reader(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:h, x:x+width] = img
                else:
                    img = hi.cv2_reader(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:y+highth, x:x+width] = img
    img = Image.fromarray(ret)
    img.save(output_wsi_path+wsi_basename+'.png')           

