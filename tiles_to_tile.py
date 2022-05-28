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
plt.switch_backend('agg')
from PIL import Image

"""
    将小块tiles拼接成大tiles，边界tiles没填充白边：
"""
# tile_path = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/v4/test_patch/'
# tiles_path='/media/ubuntu/new_computer_2T/Tiger_detection/yolov5-wanghao/runs/detect/exp2/'
# output_tile_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/v4/test_output_patch/'
# # get the list of all wsis
# tile_list = glob.glob(tile_path + '*')
# i=0
# # get a random tile from the list
# # rand_tile = np.random.randint(0,len(tile_list))
# for range_tile in range(len(tile_list)):
#     tile_file = tile_list[range_tile]
#     tile_ext = '.png'
#     tile_basename = os.path.basename(tile_file)
#     tile_basename = tile_basename[:-(len(tile_ext))]


#     tile = Image.open(tile_file)
#     [w,h,k]=np.array(tile).shape

#     highth =224
#     width=224

#     ret  = np.zeros([h,w,3],dtype = np.uint8)

#     i=i+1

#     File_Path = tiles_path

#     for x in tqdm(range(0,w,width)):
#         if x+width > w:
        
#             for y in range(0,h,highth):
#                 if y+highth > h:
                    
#                     img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
#                     ret[y:h, x:w] = img
#                 else:
#                     img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
#                     ret[y:y+highth, x:w] = img
#         else:
#             for y in range(0,h,highth):
#                 if y+highth > h:
                    
#                     img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
#                     ret[y:h, x:x+width] = img
#                 else:
#                     img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
#                     ret[y:y+highth, x:x+width] = img
#     img = Image.fromarray(ret)
#     img.save(output_tile_path+tile_basename+'.png')           







"""
    将小块tiles拼接成大tiles，边界tiles填充了白边：
"""
tile_path = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/view_patch/'
tiles_path='/media/ubuntu/new_computer_2T/Tiger_detection/yolov5-wanghao/runs/detect/exp/'
output_tile_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/view_output/'
# get the list of all wsis
tile_list = glob.glob(tile_path + '*')
i=0
# get a random tile from the list
# rand_tile = np.random.randint(0,len(tile_list))
for range_tile in range(len(tile_list)):
    tile_file = tile_list[range_tile]
    tile_ext = '.png'
    tile_basename = os.path.basename(tile_file)
    tile_basename = tile_basename[:-(len(tile_ext))]


    tile = Image.open(tile_file)
    [h,w,k]=np.array(tile).shape

    highth =224
    width=224

    ret  = np.zeros([h,w,3],dtype = np.uint8)

    i=i+1

    File_Path = tiles_path

    # File_Path="/media/ubuntu/new_computer_2T/Tiger_detection/yolov5-wanghao/runs/detect/exp/"
    # tile_basename="181S_[34272,32152,35623,33367]"


    for x in tqdm(range(0,w,width)):
        if x+width > w:
        
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:h, x:w] = img[0:h-y, 0:w-x]
                else:
                    img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:y+highth, x:w] = img[:, 0:w-x]
        else:
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:h, x:x+width] = img[0:h-y, :]
                else:
                    img = hi.cv2_reader(File_Path+tile_basename +'_'+str(x)+'_'+str(y)+".png")
                    ret[y:y+highth, x:x+width] = img


    # for x in tqdm(range(0,w,width)):
    #     if x+width > w:
        
    #         for y in range(0,h,highth):
    #             if y+highth > h:
                    
    #                 img = hi.cv2_reader(File_Path+tile_basename +'_'+str(int(x/width))+'_'+str(int(y/highth))+".png")
    #                 ret[y:h, x:w] = img[0:h-y, 0:w-x]
    #             else:
    #                 img = hi.cv2_reader(File_Path+tile_basename +'_'+str(int(x/width))+'_'+str(int(y/highth))+".png")
    #                 ret[y:y+highth, x:w] = img[:, 0:w-x]
    #     else:
    #         for y in range(0,h,highth):
    #             if y+highth > h:
                    
    #                 img = hi.cv2_reader(File_Path+tile_basename +'_'+str(int(x/width))+'_'+str(int(y/highth))+".png")
    #                 ret[y:h, x:x+width] = img[0:h-y, :]
    #             else:
    #                 img = hi.cv2_reader(File_Path+tile_basename +'_'+str(int(x/width))+'_'+str(int(y/highth))+".png")
    #                 ret[y:y+highth, x:x+width] = img



    img = Image.fromarray(ret)
    img.save(output_tile_path+tile_basename+'.png') 
