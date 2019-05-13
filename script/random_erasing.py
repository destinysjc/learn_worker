from __future__ import absolute_import
import os
import cv2
import operator
#from torchvision.transforms import *
from PIL import Image
import random
import math
import numpy as np
from xml.etree.ElementTree import SubElement, Element, ElementTree
#import torch



def read_img(jpg_path):
    img = cv2.imread(jpg_path)
    #img = np.array(img, dtype=float)
    return img


class RandomErasing(object):
    '''
    Class that performs Random Erasing in Random Erasing Data Augmentation by Zhong et al. 
    -------------------------------------------------------------------------------------
    probability: The probability that the operation will be performed.
    sl: min erasing area
    sh: max erasing area
    r1: min aspect ratio
    mean: erasing value
    -------------------------------------------------------------------------------------
    '''
    def __init__(self, probability = 0.9, sl = 0.02, sh = 0.4, r1 = 0.3, mean=[0.4914, 0.4822, 0.4465]):
        self.probability = probability
        self.mean = mean
        self.sl = sl
        self.sh = sh
        self.r1 = r1
       
    def __call__(self, img):

        rand0_1 = random.uniform(0, 1)
        print(rand0_1)
        print(self.probability)
        if  rand0_1 > self.probability:
            return img

        for attempt in range(100):
            #area = img.size()[1] * img.size()[2]
            area = img.shape[0] * img.shape[1]
            
       
            target_area = random.uniform(self.sl, self.sh) * area
            aspect_ratio = random.uniform(self.r1, 1/self.r1)

            h = int(round(math.sqrt(target_area * aspect_ratio)))
            w = int(round(math.sqrt(target_area / aspect_ratio)))
            
            
            if w < img.shape[1] and h < img.shape[0]:
                
                x1 = random.randint(0, img.shape[0] - h)
                y1 = random.randint(0, img.shape[1] - w)
                
                if img.shape[2] == 3:
                    
                    img[x1:h+x1, y1:w+y1, 0] = self.mean[0]
                    img[x1:h+x1, y1:w+y1, 1] = self.mean[1]
                    img[x1:h+x1, y1:w+y1, 2] = self.mean[2]
                else:
                    img[x1:x1+h, y1:y1+w, 0] = self.mean[0]
                    print("::::::",img)
                return img

        return img



if __name__ == "__main__":
    jpg_path = '../image/apple/bz_apple_308.jpg'
    img = read_img(jpg_path)
 
    random_e = RandomErasing()
    img_1 = random_e.__call__(img)
    
    cv2.imwrite("./test_0.jpg", img_1)