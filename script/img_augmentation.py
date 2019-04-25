import shutil
import cv2
import os
import re
import tensorflow as tf

# get file_name, file_path
def get_file_name_path(dir_file, format_key):
    jpg_file_name = []
    jpg_file_path = []
    for root, dirs, files in os.walk(dir_file):
        for f in files:
            if format_key in f:
                fp = os.path.join(root, f)
                jpg_file_name.append(f)
                jpg_file_path.append(fp)
    print("------------")
    print(jpg_file_name)
    print(jpg_file_path)
    print("-------------")
            
    return jpg_file_name, jpg_file_path

#随机设置图片的亮度
def rand_brightness(jpg_path, xml_path):
    img = cv2.imread(jpg_path)
    random_brightness = tf.image.random_brightness(img,max_delta=30)
    cv2.imwrite("brightness" + jpg_path, img)
    xml_file = re.split("/", xml_path)
    shutil.copy(xml_path, )

#随机设置图片的对比度
def rand_contrast(jpg_path, xml_path):
    img = cv2.imread(jpg_path)
    random_contrast = tf.image.random_contrast(img,lower=0.2,upper=1.8)
    cv2.imwrite("contrast" + jpg_path, img)

#随机设置图片的色度
def rand_hue(jpg_path, xml_path):
    img = cv2.imread(jpg_path)
    random_hue = tf.image.random_hue(img,max_delta=0.3)
     cv2.imwrite("hue" + jpg_path, img)

#随机设置图片的饱和度
def rand_saturation(jpg_path, xml_path):
    img = cv2.imread(jpg_path)
    random_satu = tf.image.random_saturation(img,lower=0.2,upper=1.8)
    cv2.imwrite("saturation" + jpg_path, img)
