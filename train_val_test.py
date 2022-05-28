import glob
import os
import random
import shutil

import numpy as np

input_image_path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/all_images/"
input_label_path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/all_labels/"
save_train_path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/images/train_new3/"
save_train_path_lab = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/labels/train_new3/"
save_val_path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/images/val_new3/"
save_val_path_lab = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/labels/val_new3/"
save_test_path = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/images/val_new3/"
save_test_path_lab = "/media/ubuntu/new_computer_2T/Tiger_detection/dataset/tiger-cells-detection-v6/labels/val_new3/"


# X:含label的数据集：分割成训练集和测试集
# test_size:测试集占整个数据集的比例
def train_test_val_split(input_image_path, input_label_path, img_train_dir, label_train_dir, img_test_dir,
                         label_test_dir, img_val_dir, label_val_dir, train_rate=0.65, test_rate=0.2, val_rate=0.15):
    image_list = os.listdir(input_image_path)
    image_number = len(image_list)
    train_number = int(image_number * train_rate)
    train_sample = random.sample(image_list, train_number)
    not_train_sample = list(set(image_list) - set(train_sample))
    not_train_number = len(not_train_sample)
    test_val_rate = test_rate / (test_rate + val_rate)
    test_number = int(not_train_number * test_val_rate)
    test_sample = random.sample(not_train_sample, test_number)
    val_sample = list(set(not_train_sample) - set(test_sample))
    for file_name in train_sample:
        file_name = file_name[:-4]
        img_name = input_image_path + file_name + ".png"
        img_dst = img_train_dir + file_name + ".png"
        shutil.copyfile(img_name, img_dst)
        label_name = input_label_path + file_name + ".txt"
        label_dst = label_train_dir + file_name + ".txt"
        shutil.copyfile(label_name, label_dst)
    for file_name in test_sample:
        file_name = file_name[:-4]
        img_name = input_image_path + file_name + ".png"
        img_dst = img_test_dir + file_name + ".png"
        shutil.copyfile(img_name, img_dst)
        label_name = input_label_path + file_name + ".txt"
        label_dst = label_test_dir + file_name + ".txt"
        shutil.copyfile(label_name, label_dst)
    for file_name in val_sample:
        file_name = file_name[:-4]
        img_name = input_image_path + file_name + ".png"
        img_dst = img_val_dir + file_name + ".png"
        shutil.copyfile(img_name, img_dst)
        label_name = input_label_path + file_name + ".txt"
        label_dst = label_val_dir + file_name + ".txt"
        shutil.copyfile(label_name, label_dst)


train_test_val_split(input_image_path, input_label_path, save_train_path, save_train_path_lab, save_test_path,
                         save_test_path_lab, save_val_path, save_val_path_lab, 0.8, 0.1, 0.1)