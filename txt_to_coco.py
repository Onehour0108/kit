import json
import os
from PIL import Image
import pandas as pd

class_list = ['cell']

anno_dir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/labels/val'
img_dir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v4/images/val'
json_save_dir = '/media/ubuntu/new_computer_2T/Tiger_detection/dataset/FCOS-dataset/labels'
if not os.path.exists(json_save_dir):
    os.mkdir(json_save_dir)
json_save_path = os.path.join(json_save_dir,'val.json')

'''
{"type": 'instance',
 "annotations":[{"segmentation":[[]],"bbox":[],"category_id":int,"area":float,"image_id":int,"id":int,"iscrowd":0},...,{}],
 "images":[{"file_name":str,"height":600,"width":600,"id":int}],
 "categories":[{"id":int,"name":str}]
}
'''


def txt2coco(my_json):
    img_list = os.listdir(img_dir)
    img_list.sort()

    anno_list = os.listdir(anno_dir)
    anno_list.sort()
    my_json["info"] = ''
    my_json["annotations"] = []
    my_json["images"] = []
    my_json["categories"] = []
    instance_id = 0
    for i, img in enumerate(img_list):
        img_file = os.path.join(img_dir,img)
        image_ = Image.open(img_file)
        image = {}
        image["id"] = i
        image["file_name"] = img
        image["height"] = image_.height
        image["width"] = image_.width
        
        my_json["images"].append(image)
        anno_path = os.path.join(anno_dir,anno_list[i])
        # txt_input = pd.read_table(anno_path,header = None,names=list('a'))
        # for j in range(len(txt_input)):         #遍历每一行
        #     boxes=txt_input['a'][j].split() #分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
        with open (anno_path,'r') as f:
            boxes = [line.strip().split(' ') for line in f.readlines()]
        f.close()
        for ann in boxes:
            annotation = {}
            # annotation["segmentation"] = [[]]
            annotation["iscrowd"] = 0
            annotation["image_id"] = i
            annotation["id"] = instance_id
            box = [float(num) for num in ann[:5]]
            # ann[8] = class_list.index(ann[8])+1
            # print(ann)
            annotation["category_id"] = 1
            annotation["area"] = 256
            annotation["bbox"] = [round(box[1]*224-box[3]*112),round(box[2]*224-box[4]*112),round(box[3]*224),round(box[4]*224)]
            
            my_json["annotations"].append(annotation)
            instance_id+=1

    for i_cat, cat in enumerate(class_list):
        category = {}
        category["id"] = i_cat+1
        category["name"] = cat
        my_json["categories"].append(category)
    data=json.dumps(my_json, indent=1)
    with open(json_save_path,'w',newline='\n') as f:
        # json.dump(my_json,f)
        f.write(data)
        

    

if __name__ == '__main__':
    my_json = {}
    txt2coco(my_json)
