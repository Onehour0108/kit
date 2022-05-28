import sys
sys.path.append('../')

import numpy as np
import os
import glob
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import scipy.io as sio
import cv2
import json
import openslide
import scipy
from tqdm import tqdm

from skimage import io
from openslide.deepzoom import DeepZoomGenerator



wsi_path = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/ljc_test/img_10x/'
tile_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/ljc_test/tiles/'

# get the list of all wsis
wsi_list = glob.glob(wsi_path + '*')
i=0
# get a random wsi from the list
# rand_wsi = np.random.randint(0,len(wsi_list))
for rand_wsi in range(len(wsi_list)):
    wsi_file = wsi_list[rand_wsi]
    wsi_ext = '.tif'

    wsi_basename = os.path.basename(wsi_file)
    wsi_basename = wsi_basename[:-(len(wsi_ext))]


    slide = openslide.open_slide(wsi_file)

    highth =1600
    width=1600
    # data_gen = DeepZoomGenerator(slide, tile_size=highth, overlap=0, limit_bounds=False)


    [w,h]=slide.level_dimensions[0]
    print(w)
    print(h)
    # H = slide.level_dimensions[0][0]
    # W = slide.level_dimensions[0][1]
    # print(w,h)
    # num_w = int(np.floor(w/width))+1
    # num_h = int(np.floor(h/highth))+1
    i=i+1

    import os
    File_Path = tile_path+str(i)+'/'      #获取到当前文件的目录，并检查是否有report文件夹，如果不存在则自动新建report文件
    if not os.path.exists(File_Path):
        os.makedirs(File_Path)

    for x in tqdm(range(0,w,width)):
        if x+width > w:
        
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    subimg = slide.read_region((x,y),level=0,size=(w-x,h-y)).convert('RGB')
                    subimg.save(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
                else:
                    subimg = slide.read_region((x,y),level=0,size=(w-x,highth)).convert('RGB')
                    subimg.save(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
        else:
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    subimg = slide.read_region((x,y),level=0,size=(width,h-y)).convert('RGB')
                    subimg.save(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
                else:
                    subimg = slide.read_region((x,y),level=0,size=(width,highth)).convert('RGB')
                    subimg.save(File_Path+wsi_basename +'_'+str(x)+'_'+str(y)+".png")
        


    # for i in range(num_w):
    #     for j in range(num_h):

    #         img = np.array(data_gen.get_tile(data_gen.level_count-1, (i, j))) #切
    #         plt.imshow(img)
    #         plt.xticks([])
    #         plt.yticks([])
    #         plt.axis('off')
    #         plt.savefig('/home/ubuntu/output/Gli/in2/'+wsi_basename +'_'+str(i)+'_'+str(j)+".png",bbox_inches='tight',pad_inches=0.0,dpi=2500)
print('done')