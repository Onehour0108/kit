from PIL import Image
import os
import math
from tqdm import tqdm

"""将图片切割成等份"""
# path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/test/test_patch" #文件夹目录
# files= os.listdir(path) #得到文件夹下的所有文件名称
# for file in files:
#     img_file=path+"/"+file
#     file_name=file[:-4]
#     img = Image.open(img_file)
#     size = img.size
#     #print(size)

#     # 准备将图片切割成100张小图片
#     weight = int(size[0] // 20)
#     height = int(size[1] // 20)
#     # 切割后的小图的宽度和高度
#     #print(weight, height)

#     for j in range(20):
#         for i in range(20):
#             box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
#             region = img.crop(box)
#             region.save('/media/ubuntu/new_computer_2T/Tiger_detection/dataset/test/test_tiles'+'/'+file_name+'_'+str(int(i*weight))+'_'+str(int(j*height))+'.png')


"""将图片切割成规定大小"""
path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/view_patch" #文件夹目录
output_path='/media/ubuntu/new_computer_2T/Tiger_detection/dataset/visualization/view_tiles'
files= os.listdir(path) #得到文件夹下的所有文件名称
for file in tqdm(files):
    img_file=path+"/"+file
    file_name=file[:-4]
    img = Image.open(img_file)
    [w,h] = img.size
    #print(size)

    
    highth =224
    width=224
#     # 切割后的小图的宽度和高度
#     #print(weight, height)
#     from tqdm import tqdm
#     for x in tqdm(range(0,w,width)):
#         if x+width > w:
#             x=w-width
#         for y in range(0,h,highth):
#             if y+highth > h:
#                 y=h-highth
#             box = (x, y, x + width, y + highth)
#             region = img.crop(box)
#             region.save(output_path+'/'+file_name+'_'+str(int(math.ceil(x/width)))+'_'+str(int(math.ceil(y/highth)))+'.png')
        
    
    
    for x in range(0,w,width):
        if x+width > w:
        
            for y in range(0,h,highth):
                if y+highth > h:
                    box = (x, y, w, h)
                    region = img.crop(box)
                    new_image = Image.new('RGB', (width,highth), (0, 0, 0))
                    new_image.paste(region,(0,0))
                    new_image.save(output_path+'/'+file_name+'_'+str(int(x))+'_'+str(int(y))+'.png')
                    
                else:
                    box = (x, y, w, y+highth)
                    region = img.crop(box)
                    new_image = Image.new('RGB', (width,highth), (0, 0, 0))
                    new_image.paste(region,(0,0))
                    new_image.save(output_path+'/'+file_name+'_'+str(int(x))+'_'+str(int(y))+'.png')
        else:
            for y in range(0,h,highth):
                if y+highth > h:
                    
                    box = (x, y, x+width, h)
                    region = img.crop(box)
                    new_image = Image.new('RGB', (width,highth), (0, 0, 0))
                    new_image.paste(region,(0,0))
                    new_image.save(output_path+'/'+file_name+'_'+str(int(x))+'_'+str(int(y))+'.png')
                else:
                    box = (x, y, x+width, y+highth)
                    region = img.crop(box)
                    region.save(output_path+'/'+file_name+'_'+str(int(x))+'_'+str(int(y))+'.png')     



"""填充图片为规定大小"""
# path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v0/images/val" #文件夹目录
# output_path="/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v1/images/val_nor"
# files= os.listdir(path) #得到文件夹下的所有文件名称
# for file in files:
#     img_file=path+"/"+file
    
#     img = Image.open(img_file)
#     size = img.size
#     #print(size)
#     w = 352
#     height = 352

#     new_image = Image.new('RGB', (w,height), (255, 255, 255))
#     new_image.paste(img,(0,0))

#     new_image.save(output_path+"/"+file)