from genericpath import exists
import os
import shutil
from turtle import width
import numpy as np
import pandas as pd
import math
import os
from tqdm import tqdm

'''将两个文件夹中的同名文件夹找到'''
# srcdir = 'test_normalization'
# srcdir2 = 'abso_copy'
# dstdir = 'tmp'
# with open('exists.txt','w+') as f:
#     for _,_,files in os.walk(srcdir):
#         for file in sorted(files):
#             if exists(os.path.join(srcdir2,file)):
#                 # print(file)
#                 src = os.path.join(srcdir2,file)
#                 dst = os.path.join(dstdir,file)
#                 f.write(file+'\n')
#                 shutil.copy2(src=src,dst=dst)

'''将两个文件夹中的名字前缀相同文件夹找到'''
srcdir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/all_images'
srcdir2 = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/labels/train'
dstdir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/labels/temp2'
with open('exists.txt','w+') as f:
    for _,_,files in os.walk(srcdir):
          for file in sorted(files):
            if exists(srcdir2+'/'+file[:-4]+'.txt'):
                # print(file)
                src = srcdir2+'/'+file[:-4]+'.txt'
                dst = dstdir+'/'+file[:-4]+'.txt'
                f.write(file+'\n')
                shutil.copy2(src=src,dst=dst)



# srcdir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/pre_gt2'
# srcdir2 = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v2/images/train_test'
# dstdir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/test_newtrain2'
# with open('exists.png','w+') as f:
#     for _,_,files in os.walk(srcdir):
#         for file in sorted(files):
#             if exists(srcdir2+'/'+file[:-4]+'.png'):
#                 # print(file)
#                 src = srcdir2+'/'+file[:-4]+'.png'
#                 dst = dstdir+'/'+file[:-4]+'.png'
#                 f.write(file+'\n')
#                 shutil.copy2(src=src,dst=dst)


'''统计txt文件中行数'''
# def readline_count(file_name):

#     return len(open(file_name).readlines())


# path="/media/ubuntu/new_computer_2T/Tiger_detection/dataset/3.10/labels/train"
# files= os.listdir(path)
# num=0
# for file in files:
#     num +=readline_count(os.path.join(path,file))
# print(num)



'''统计txt文件的行数区间'''
# def readline_count(file_name):

#     return len(open(file_name).readlines())


# path="/media/ubuntu/new_computer_2T/Tiger_detection/dataset/3.11/labels/val"
# files= os.listdir(path)
# line=[]
# for file in files:
#     line.append(readline_count(os.path.join(path,file)))
# print(len([i for i in line if i==0]))  #txt中0行的文件个数
# print(len([i for i in line if (i<=20 and i>0)]))
# print(len([i for i in line if (i>20 and i<=100)]))
# print(len([i for i in line if i>100]))


'''将txt文件内数据运算后保存文件'''
# path_input = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/test/big_labels" #文件夹目录
# path_output = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/test/small_labels" #文件夹目录
# tiles_input="/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/test/big_tiles"
# files_input= os.listdir(path_input) #得到文件夹下的所有文件名称

# for file_input in tqdm(files_input): #遍历文件夹
#     txt_input = path_input+'/'+ file_input
#     txt_output = path_output+'/'+ file_input[:-4]
#     tile_input=tiles_input+'/'+ file_input[:-4]+'.png'
#     from PIL import Image
#     img=Image.open(tile_input)
#     img_size=img.size
#     [w,h]=img_size
#     width=224
#     highth=224
#     txt_input = pd.read_table(txt_input,header = None,names=list('a'))
    
#     for x in range(0,w,width):
#         for y in range(0,h,highth):
#             open(txt_output +'_'+str(int(x/width))+'_'+str(int(y/width))+ '.txt', 'a')
#     for j in range(len(txt_input)):         #遍历每一行
#         coordinate_input=txt_input['a'][j].split() #分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表

#         m=math.floor(float(coordinate_input[1])*w/width)
#         n=math.floor(float(coordinate_input[2])*h/highth)
#         line=(int(coordinate_input[0]),(float(coordinate_input[1])*w-width*m)/width,(float(coordinate_input[2])*h-highth*n)/highth,16/width,16/highth)
#         with open(txt_output +'_'+str(m)+'_'+str(n)+ '.txt', 'a') as f:
#             f.write(('%g ' * len(line)).rstrip() % line + '\n')


    #图片等分对应labels
    # for p in range(4):
    #     for q in range(4):
    #         open(txt_output +str(p)+'_'+str(q)+ '.txt', 'a')
    # for j in range(len(txt_input)):         #遍历每一行
    #     coordinate_input=txt_input['a'][j].split() #分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
    #     m=math.floor(float(coordinate_input[1])*4)
    #     n=math.floor(float(coordinate_input[2])*4)
    #     line=(int(coordinate_input[0]),float(coordinate_input[1])*4-m,float(coordinate_input[2])*4-n,float(coordinate_input[3])*4,float(coordinate_input[4])*4)
    #     with open(txt_output +str(m)+'_'+str(n)+ '.txt', 'a') as f:
    #         f.write(('%g ' * len(line)).rstrip() % line + '\n')

'''将txt文件内数据运算后保存文件，未实现'''
# path_input = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/test/big_labels" #文件夹目录
# path_output = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/test/small_labels" #文件夹目录
# tiles_input="/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/test/big_tiles"
# files_input= os.listdir(path_input) #得到文件夹下的所有文件名称

# for file_input in tqdm(files_input): #遍历文件夹
#     txt_input = path_input+'/'+ file_input
#     txt_output = path_output+'/'+ file_input[:-4]
#     tile_input=tiles_input+'/'+ file_input[:-4]+'.png'
#     from PIL import Image
#     img=Image.open(tile_input)
#     img_size=img.size
#     [w,h]=img_size
#     width=224
#     highth=224
#     txt_input = pd.read_table(txt_input,header = None,names=list('a'))
    
#     for x in range(0,w,width):
#         for y in range(0,h,highth):
#             open(txt_output +'_'+str(int(x/width))+'_'+str(int(y/highth))+ '.txt', 'a')
#     for j in range(len(txt_input)):         #遍历每一行
#         coordinate_input=txt_input['a'][j].split() #分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
#         m=math.floor(float(coordinate_input[1])*w/width)
#         n=math.floor(float(coordinate_input[2])*h/highth)
#         #属于非边界的tiles
#         if(float(coordinate_input[1])*w<w//width*width \
#              and float(coordinate_input[2])*h<h//highth*highth):
#             line=(int(coordinate_input[0]),(float(coordinate_input[1])*w-width*m)/width,(float(coordinate_input[2])*h-highth*n)/highth,16/width,16/highth)
#             with open(txt_output +'_'+str(m)+'_'+str(n)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')
#         #x属于边界，y不属于边界
#         if(float(coordinate_input[1])*w>=w//width*width \
#              and float(coordinate_input[2])*h<h//highth*highth):
#              line=(int(coordinate_input[0]),(width+float(coordinate_input[1])*w-w)/width,(float(coordinate_input[2])*h-highth*n)/highth,16/width,16/highth)
#              with open(txt_output +'_'+str(m)+'_'+str(n)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')
#         #y属于边界，x不属于边界
#         if(float(coordinate_input[1])*w<w//width*width \
#              and float(coordinate_input[2])*h>=h//highth*highth):
#              line=(int(coordinate_input[0]),(float(coordinate_input[1])*w-width*m)/width,(highth+float(coordinate_input[2])*h-h)/highth,16/width,16/highth)
#              with open(txt_output +'_'+str(m)+'_'+str(n)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')
#         #x，y都属于边界
#         if(float(coordinate_input[1])*w>=w//width*width \
#              and float(coordinate_input[2])*h>=h//highth*highth):
#              line=(int(coordinate_input[0]),(width+float(coordinate_input[1])*w-w)/width,(highth+float(coordinate_input[2])*h-h)/highth,16/width,16/highth)
#              with open(txt_output +'_'+str(m)+'_'+str(n)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')
        
#         if(w!=w//width*width and float(coordinate_input[1])*w>w-width and float(coordinate_input[1])*w<w//width*width \
#              and float(coordinate_input[2])*h<=h//highth*highth):
#              line=(int(coordinate_input[0]),(width+float(coordinate_input[1])*w-w)/width,(float(coordinate_input[2])*h-highth*n)/highth,16/width,16/highth)
#              with open(txt_output +'_'+str(m+1)+'_'+str(n)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')

#         if(float(coordinate_input[1])*w<=w//width*width \
#              and float(coordinate_input[2])*h<h//highth*highth and float(coordinate_input[2])*h>h-highth and h!=h//highth*highth):
#              line=(int(coordinate_input[0]),(float(coordinate_input[1])*w-width*m)/width,(highth+float(coordinate_input[2])*h-h)/highth,16/width,16/highth)
#              with open(txt_output +'_'+str(m)+'_'+str(n+1)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')

#         if(w!=w//width*width and h!=h//highth*highth and float(coordinate_input[1])*w<w//width*width and float(coordinate_input[1])*w>w-width\
#              and float(coordinate_input[2])*h<h//highth*highth and float(coordinate_input[2])*h>h-highth):
#              line=(int(coordinate_input[0]),(width+float(coordinate_input[1])*w-w)/width,(highth+float(coordinate_input[2])*h-h)/highth,16/width,16/highth)
#              with open(txt_output +'_'+str(m+1)+'_'+str(n+1)+ '.txt', 'a') as f:
#                 f.write(('%g ' * len(line)).rstrip() % line + '\n')




'''重新制作标签'''
# path_input = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v1/labels/train" #文件夹目录
# tiles_input="/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v1/images/train"
# path_output = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v1/labels/train_v3" #文件夹目录
# files_input= os.listdir(path_input) #得到文件夹下的所有文件名称

# for file_input in files_input: #遍历文件夹
#     txt_input = path_input+'/'+ file_input
#     tile_input=tiles_input+'/'+ file_input[:-4]+'.png'
#     txt_output = path_output+'/'+ file_input
#     from PIL import Image
#     img=Image.open(tile_input)
#     img_size=img.size
#     txt_input = pd.read_table(txt_input,header = None,names=list('a'))
#     if(len(txt_input)==0):
#         open(txt_output, 'a')
#     for j in range(len(txt_input)):         #遍历每一行
#         coordinate_input=txt_input['a'][j].split() #分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
#         line=(int(coordinate_input[0]),float(coordinate_input[1])*img_size[0]/352,float(coordinate_input[2])*img_size[1]/352,16/352,16/352)
#         with open(txt_output, 'a') as f:
#             f.write(('%g ' * len(line)).rstrip() % line + '\n')



# path_input = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/labels/val" #文件夹目录
# path_output = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/labels/test_gt" #文件夹目录
# files_input= os.listdir(path_input) #得到文件夹下的所有文件名称

# for file_input in files_input: #遍历文件夹
#     txt_input = path_input+'/'+ file_input
#     txt_output = path_output+'/'+ file_input
#     from PIL import Image
#     txt_input = pd.read_table(txt_input,header = None,names=list('a'))
#     if(len(txt_input)==0):
#         open(txt_output, 'a')
#     for j in range(len(txt_input)):         #遍历每一行
#         coordinate_input=txt_input['a'][j].split() #分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
#         line=(float(coordinate_input[1])*224,float(coordinate_input[2])*224)
#         with open(txt_output, 'a') as f:
#             f.write(('%g ' * len(line)).rstrip() % line + '\n')            