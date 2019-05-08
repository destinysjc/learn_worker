import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import os
#from data_aug.bbox_util import *


import pickle as pkl

lib_path = os.path.join(os.path.realpath("."), "data_aug")
sys.path.append(lib_path)


class Mixup(object):

    '''
    Mixup two images for data augmentation
    src1, the path of the image1
    src2, the path of the image2

    '''

    def __init__(self, src1, src2, alpha=0.1):
        random_alpha = random.uniform(0.1, 0.9)
        self.alpha = random_alpha
        self.src1 = src1
        self.src2 = src2
    # def __call__(self, src1, src2):

    def process(self):
        # get image 1
        # print(type(self.src1))
        # print(self.src1)

        self.src1 = self.src1.strip()
        img1 = cv2.imread(self.src1)
        # print(self.src1)
        # print(img1)
        pkl1 = self.src1.split('.')[0]+'.pkl'
        bboxes1 = pkl.load(open(pkl1, "rb"))
        bboxes1_list = bboxes1.tolist()

        # make sure that image1 and image2 are not the same

        img2 = cv2.imread(self.src2)
        pkl2 = self.src2.split('.')[0]+'.pkl'
        bboxes2 = pkl.load(open(pkl2, "rb"))
        bboxes2_list = bboxes2.tolist()

        # mixup image

        h1, w1, c1 = img1.shape
        h2, w2, c2 = img2.shape

        width = max(w1, w2)
        height = max(h1, h2)

        mix_img = np.zeros(shape=(height, width, 3), dtype='float32')
        mix_img[:img1.shape[0], :img1.shape[1],
                :] = img1.astype('float32') * self.alpha
        mix_img[:img2.shape[0], :img2.shape[1],
                :] += img2.astype('float32') * (1. - self.alpha)
        mix_img = mix_img.astype('uint8')

        img = mix_img

        bboxes_list = bboxes1_list+bboxes2_list
        len1 = int(len(bboxes1_list))
        len2 = int(len(bboxes2_list))
        count = len1 + len2
        bboxes = np.reshape(np.array(bboxes_list), (count, 5))

        return img, bboxes
