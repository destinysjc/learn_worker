import os
import cv2
import shutil
import time
import numpy as np 
from PIL import Image

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
    # print("------------")
    # print(jpg_file_name)
    # print(jpg_file_path)
    # print("-------------")
            
    return jpg_file_name, jpg_file_path

def img_read(img_path, resizes):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (resizes, resizes))
    img = np.array(img, np.float32) / 255
    return img

def img_compare(original_img, original_img_path, compare_img_path, resizes):
    comp_img = img_read(compare_img_path, resizes)
    European_distance = (original_img - comp_img) ** 2
    score = np.sum(European_distance) / (resizes * resizes * 3)
    print("Difference Score:", score)
    if score < 0.05:
        shutil.copy2(compare_img_path, original_img_path)

class DHash(object):
    @staticmethod
    def calculate_hash(image):
        """
        计算图片的dHash值
        :param image: PIL.Image
        :return: dHash值,string类型
        """
        difference = DHash.__difference(image)
        # 转化为16进制(每个差值为一个bit,每8bit转为一个16进制)
        decimal_value = 0
        hash_string = ""
        for index, value in enumerate(difference):
            if value:  # value为0, 不用计算, 程序优化
                decimal_value += value * (2 ** (index % 8))
            if index % 8 == 7:  # 每8位的结束
                hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f
                decimal_value = 0
        return hash_string

    @staticmethod
    def hamming_distance(first, second):
        """
        计算两张图片的汉明距离(基于dHash算法)
        :param first: Image或者dHash值(str)
        :param second: Image或者dHash值(str)
        :return: hamming distance. 值越大,说明两张图片差别越大,反之,则说明越相似
        """
        # A. dHash值计算汉明距离
        if isinstance(first, str):
            return DHash.__hamming_distance_with_hash(first, second)

        # B. image计算汉明距离
        hamming_distance = 0
        image1_difference = DHash.__difference(first)
        image2_difference = DHash.__difference(second)
        for index, img1_pix in enumerate(image1_difference):
            img2_pix = image2_difference[index]
            if img1_pix != img2_pix:
                hamming_distance += 1
        return hamming_distance

    @staticmethod
    def __difference(image):
        """
        *Private method*
        计算image的像素差值
        :param image: PIL.Image
        :return: 差值数组。0、1组成
        """
        resize_width = 9
        resize_height = 8
        # 1. resize to (9,8)
        smaller_image = image.resize((resize_width, resize_height))
        # 2. 灰度化 Grayscale
        grayscale_image = smaller_image.convert("L")
        # 3. 比较相邻像素
        pixels = list(grayscale_image.getdata())
        difference = []
        for row in range(resize_height):
            row_start_index = row * resize_width
            for col in range(resize_width - 1):
                left_pixel_index = row_start_index + col
                difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
        return difference

    @staticmethod
    def __hamming_distance_with_hash(dhash1, dhash2):
        """
        *Private method*
        根据dHash值计算hamming distance
        :param dhash1: str
        :param dhash2: str
        :return: 汉明距离(int)
        """
        difference = (int(dhash1, 16)) ^ (int(dhash2, 16))
        return bin(difference).count("1")

if __name__ == '__main__':
    # original_img_dir = '../tmp/object365/compare_img'
    # original_img_file = '/strawberry01.jpg'
    # original_img_path = original_img_dir + original_img_file
    # compare_img_path = '../tmp/object365/train'
    # resizes = 300

    # jpg_file_name, jpg_file_path = get_file_name_path(compare_img_path, '.jpg')
    # original_img = img_read(original_img_path, resizes)
    # start = time.time()
    # for jfp in jpg_file_path:
    #     start_i = time.time()
    #     img_compare(original_img, original_img_dir, jfp, resizes)
    #     print("---------" + jfp + "---------")
    #     print('Useing Time:', time.time() - start)
    #     print(">>>>>>>>>>>>>>>---[Total]---<<<<<<<<<<<<<<<<<")
    #     print('Total Time:', time.time() - start)
    
    original_img_dir = '../tmp/object365/compare_img'
    original_img_file = '/strawberry01.jpg'
    original_img_path = original_img_dir + original_img_file
    compare_img_path = '../tmp/object365/images'
    
    original_img = Image.open(original_img_path,'r')
    dhash = DHash()
    original_hash = dhash.calculate_hash(original_img)
    jpg_file_name, jpg_file_path = get_file_name_path(compare_img_path, '.jpg')
    start = time.time()
    res_l = []
    for jfp in jpg_file_path:
        start_i = time.time()
        comp_img = Image.open(jfp, 'r')
        comp_hash = dhash.calculate_hash(comp_img)
        res = dhash.hamming_distance(original_hash, comp_hash)
        #res_l.append(res)
        if res < 15:
            print('~~~~~~~~~~~~~~~~~~', compare_img_path, "Copy To:", original_img_dir)
            shutil.copy2(jfp, original_img_dir)
            

        print('Every Image Useing Time:', time.time() - start_i, 'res:', res)
        print('----------[', jfp, '}------------')
        print('Total Time:', time.time() - start)
        
    
    
