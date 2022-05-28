import spams
import numpy as np
import cv2
import time
import os
import glob
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from PIL import Image


STAIN_NUM=2
THRESH=0.9
LAMBDA1=0.01
LAMBDA2=0.01
ITER=100
fast_mode=0
getH_mode=0

def getV(img):
    
    I0 = img.reshape((-1,3)).T
    I0[I0==0] = 1
    V0 = np.log(255 / I0)

    img_LAB = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    mask = img_LAB[:, :, 0] / 255 < THRESH
    I = img[mask].reshape((-1, 3)).T
    I[I == 0] = 1
    V = np.log(255 / I)

    return V0, V


def getW(V):
    W = spams.trainDL(np.asfortranarray(V), K=STAIN_NUM, lambda1=LAMBDA1, iter=ITER, mode=2, modeD=0, posAlpha=True, posD=True, verbose=False)
    W = W / np.linalg.norm(W, axis=0)[None, :]
    if (W[0,0] < W[0,1]):
        W = W[:, [1,0]]
    return W


def getH(V, W):
    if (getH_mode == 0):
        H = spams.lasso(np.asfortranarray(V), np.asfortranarray(W), mode=2, lambda1=LAMBDA2, pos=True, verbose=False).toarray()
    elif (getH_mode == 1):
        H = np.linalg.pinv(W).dot(V)
        H[H<0] = 0
    else:
        H = 0
    return H


def stain_separate(img):
    start = time.time()
    if (fast_mode == 0):
        V0, V = getV(img)
        W = getW(V)
        H = getH(V0, W)
    elif (fast_mode == 1):
        m = img.shape[0]
        n = img.shape[1]
        grid_size_m = int(m / 5)
        lenm = int(m / 20)
        grid_size_n = int(n / 5)
        lenn = int(n / 20)
        W = np.zeros((81, 3, STAIN_NUM)).astype(np.float64)
        for i in range(0, 4):
            for j in range(0, 4):
                px = (i + 1) * grid_size_m
                py = (j + 1) * grid_size_n
                patch = img[px - lenm : px + lenm, py - lenn: py + lenn, :]
                V0, V = getV(patch)
                W[i*9+j] = getW(V)
        W = np.mean(W, axis=0)
        V0, V = getV(img)
        H = getH(V0, W)
    print('stain separation time:', time.time()-start, 's')
    return W, H


from PIL import Image
import math



tile_path = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v3/images/val_nor/'
output_tile_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v3/images/val_h_nor/'
# get the list of all wsis
tile_list = glob.glob(tile_path + '*')
# get a random tile from the list
# rand_tile = np.random.randint(0,len(tile_list))
for range_tile in range(len(tile_list)):
    tile_file = tile_list[range_tile]
    tile_ext = '.png'
    tile_basename = os.path.basename(tile_file)
    tile_basename = tile_basename[:-(len(tile_ext))]
    img = cv2.imread(tile_file)
    # img = cv2.imread(tile_path+'240S_[35788,27713,37163,28965]_1_5.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    w,h=stain_separate(img)
    h=h[0,:]
    h=h.reshape(224,224)
    h[h>1]=1
    # h[h<0]=0

    # temp2=h*255
    # temp2=Image.fromarray(np.uint8(temp2))
    # temp2.save("6.png")

    temp=np.zeros((224,224,3))
    temp[:,:,0]=np.array(255-img[:,:,0])*np.array(h)
    temp[:,:,1]=np.array(255-img[:,:,1])*np.array(h)
    temp[:,:,2]=np.array(255-img[:,:,2])*np.array(h) 
    
    temp[temp>255]=255
    temp[temp<0]=0
    temp=255-temp   
    temp=Image.fromarray(np.uint8(temp))
    # temp.save("5.png")
    temp.save(output_tile_path+tile_basename+'.png')
    
    # h*=255
    # h[h>255]=255
    # # for i in range(224):
    # #     for j in range(224):
    # #         if(h[i,j]>255):
    # #             h[i,j]=255
    # h=255-h
    # temp=np.zeros((224,224,4))
    # temp[:,:,0:3]=img
    # temp[:,:,-1]=h
    # h_output = Image.fromarray(np.uint8(h))
    # h_output.convert('L').save(output_tile_path+tile_basename+'.png')
