import os
import csv
import re
import cv2
#import matplotlib.pyplt as plt
import numpy as np 
import xml.etree.ElementTree as ET
from data_normal import write_voc_xml

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




# 将*.txt存入list
def write_class_l(file_path):
    label_info = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for l in lines:
            l = l.split()
            name = l[0]
            size = l[1:3]
            box = l[3:]
            size = list(map(int, size))
            boxs = list(map(float, box))
            n = int(len(boxs)/4)
            boxes = np.array(boxs).reshape(n, 4)
            label_info.append(name)
            label_info.append(size)
            label_info.append(boxes)
        
    return label_info
        
# generate *.xml
def write_voc_xml(txt_path):
    
    classes_ = re.split(r"/", txt_path)
    classes = classes_[-2]
    #print(classes_)
    label_info = write_class_l(txt_path)
    file_path = classes_[-1][:-4] + ".jpg"
    annotation =ET.Element('annotation')

    folder = ET.SubElement(annotation, 'folder')
    folder.text = 'voc2012'

    filename2 = ET.SubElement(annotation, 'filename')
    filename2.text = file_path


    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database')
    database.text = 'Unknown'

    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(label_info[1][0])
    height = ET.SubElement(size, 'height')
    height.text = str(label_info[1][1])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(3)

    segment = ET.SubElement(annotation, 'segment')
    segment.text = '0'
    for i in range(len(label_info[2])):
        ob = ET.SubElement(annotation, 'object')
        name = ET.SubElement(ob, 'name')
        name.text = str(classes)
        pose = ET.SubElement(ob, 'pose')
        pose.text = 'Unspecified'
        truncated =ET.SubElement(ob, 'truncated')
        truncated.text = 0
        difficult = ET.SubElement(ob, 'difficult')
        difficult.text = 0

        bndbox = ET.SubElement(ob, 'bndbox')
        #print(label_info[2][i])
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(int(label_info[2][i][0] * label_info[1][0]))
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(int(label_info[2][i][2] * label_info[1][1]))
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(int(label_info[2][i][1] * label_info[1][0]))
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(int(label_info[2][i][3] * label_info[1][1]))
    #print(txt_path[-4])
    xml_path = txt_path[:-4] + '.xml'
    #print(xml_path)
    tree = ET.ElementTree(annotation)
    tree.write(xml_path)

# draw box bunding
def draw_box(jpg_path, ana_path):
    label_info = write_class_l(ana_path)
    print(label_info)
    xmin = int(label_info[2][0][0] * label_info[1][0])
    ymin = int(label_info[2][0][2] * label_info[1][1])
    xmax = int(label_info[2][0][1] * label_info[1][0])
    ymax = int(label_info[2][0][3] * label_info[1][1])
    print(xmin, ymin, xmax, ymax)
    img = cv2.imread(jpg_path)
    img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (55,255,155), 4)
    #plt.imshow(img,'brg')
    #font = cv2.FONT_HERSHEY_SUPLEX
    text = '001'
    #cv2.putText(img, text, (212, 310), 2, (55,0,255), 1)
    cv2.imwrite('001_ne.jpg', img)


if __name__ == "__main__":
    txt_path = r'../workTrains/train_ssdlite/image/dataVoc/'
    xml_file_name, xml_file_path = get_file_name_path(txt_path, format_key='.txt')
    for fp in xml_file_path:
        
        write_voc_xml(fp)
        print(fp)
    
    #write_voc_xml(txt_path)
    #draw_box(r'C:/Users/Administrator/Desktop/dataVoc/Flower/8a0deab74c4d6dc9.jpg', txt_path)
