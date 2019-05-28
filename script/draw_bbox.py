import os
import re
import json
import cv2
import shutil
import numpy as np 


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
def read_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        f_info = []
        for line in lines:
            line = line.strip("\n").split(" ")
            f_info.append(line)
    print(f_info)
    return f_info

# draw box bunding
def draw_box(f_info, file_path):
    f_info = np.array(f_info)
    f_path = f_info[0][0]
    wide = float(f_info[0][1])
    length = float(f_info[0][2])
    depth = f_info[0][3]
    
    print(f_info.shape)
    ll = len(f_info)
    print(ll)
    if len(f_info) > 1:
        label = f_info[1][0]
        if f_info[1][1].isalpha() == True:
            print("Skiping!!!")

        else:
            xmin = int(float(f_info[1][1]) * wide)
            ymin = int(float(f_info[1][2]) * length)
            xmax = int(float(f_info[1][3]) * wide)
            ymax = int(float(f_info[1][4]) * length)
            jpg_path = "." + file_path.split(".")[1] + ".jpg"
            img = cv2.imread(jpg_path)
            img = cv2.rectangle(img, (xmin, ymax), (xmax, ymin), (55,255,155), 4)
            #plt.imshow(img,'brg')
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(img, label, (xmin-2, ymax-1), font, 1, (3,3,255), 1)
            #cv2.putText(img, text, (212, 310), 2, (55,0,255), 1)
            cv2.imwrite(jpg_path, img)
            print("Save Path:", jpg_path)


    
if __name__ == "__main__":
    txt_path = "./model190522/filtered_apple"
    txt_file_name, txt_file_path = get_file_name_path(txt_path, ".txt")
    for txt_fp in txt_file_path:
        f_info = read_file(txt_fp)
        draw_box(f_info, txt_fp)
        print("***********")
        