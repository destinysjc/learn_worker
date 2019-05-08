from data_aug.data_aug import *
from data_aug.bbox_util import *
import cv2 
import pickle as pkl
import numpy as np 
import matplotlib.pyplot as plt


import os
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, ElementTree




class_dict={"0":"apple", "1":"banana", "2":"orange", "3":"pineapple", "4":"cake", "5":"pizza", "6":"pear", "7":"bread", "8":"strawberry", "9":"pudding", "10":"ice", "11":"mango","12":"macaron", "13":"sandwich", "14":"peach"}


def gen_transform_img_ann( img_path, pkl_path, new_img_path, xml_path ):
    ##img = cv2.imread(img_path)[:,:,::-1] #OpenCV uses BGR channels
    img = cv2.imread(img_path)
    bboxes = pkl.load(open(pkl_path, "rb"))
    ## we need to get rid of the invalide boundingbox and images 
    if not img.shape:
        return
    if not bboxes.shape:
        return


    ### transform
    transforms = Sequence([RandomHorizontalFlip(1), RandomScale(0.2, diff = True), RandomRotate(10), 
RandomShear(0.2)])	
    img, bboxes = transforms(img, bboxes)


    row, col = bboxes.shape
    img_height, img_width,channels = img.shape



    annotation = Element('annotation')

    folder = SubElement(annotation, 'folder')
    folder.text = "label"

    filename2 = SubElement(annotation, 'filename')
    filename2.text = "trans_"+pkl_path.split(".")[0]+".jpg"

    path2 = SubElement(annotation, 'path')
    path2.text = pkl_path.split(".")[0]+".jpg"

    source = SubElement(annotation, 'source')
    database = SubElement(source, 'database')
    database.text = 'Unknown'

    size = SubElement(annotation, 'size')
    width = SubElement(size, 'width')
    width.text = str(img_width)
    height = SubElement(size, 'height')
    height.text = str(img_height)
    depth = SubElement(size, 'depth')
    depth.text = "3"

    segment = SubElement(annotation, 'segment')
    segment.text = '0'






    for Row in range(row):
        ob = SubElement(annotation, 'object')
        name = SubElement(ob, 'name')
        #name.text = str(bboxes[Row][4])
        name.text = str(class_dict[str(int(bboxes[Row][4]))])
        pose = SubElement(ob, 'pose')
        pose.text = 'Unspecified'
        truncated = SubElement(ob, 'truncated')
        truncated.text = '0'
        difficult = SubElement(ob, 'difficult')
        difficult.text = '0'

        bndbox = SubElement(ob, 'bndbox')
        xmin = SubElement(bndbox, 'xmin')
        xmin.text = str(int(bboxes[Row][0]))
        ymin = SubElement(bndbox, 'ymin')
        ymin.text = str(int(bboxes[Row][1]))
        xmax = SubElement(bndbox, 'xmax')
        xmax.text = str(int(bboxes[Row][2]))
        ymax = SubElement(bndbox, 'ymax')
        ymax.text = str(int(bboxes[Row][3]))	

        #for Row in range(row):
    # Row = 0
    # ob = SubElement(annotation, 'object')
    # name = SubElement(ob, 'name')
    # name.text = str(bboxes[Row][4])
    # pose = SubElement(ob, 'pose')
    # pose.text = 'Unspecified'
    # truncated = SubElement(ob, 'truncated')
    # truncated.text = '0'
    # difficult = SubElement(ob, 'difficult')
    # difficult.text = '0'

    # bndbox = SubElement(ob, 'bndbox')
    # xmin = SubElement(bndbox, 'xmin')
    # xmin.text = str(bboxes[Row][0])
    # ymin = SubElement(bndbox, 'ymin')
    # ymin.text = str(bboxes[Row][1])
    # xmax = SubElement(bndbox, 'xmax')
    # xmax.text = str(bboxes[Row][2])
    # ymax = SubElement(bndbox, 'ymax')
    # ymax.text = str(bboxes[Row][3])  	



    tree = ElementTree(annotation)
    tree.write(xml_path, encoding='utf-8')




    ### save the transformed image
    cv2.imwrite(new_img_path,img)






#
# def gen_xml(xml_path, newname, label, img_width, img_height, Xmin, Ymin, Xmax, Ymax):
#     annotation = Element('annotation')

#     folder = SubElement(annotation, 'folder')
#     folder.text = folder_name

#     filename2 = SubElement(annotation, 'filename')
#     filename2.text = newname

#     path2 = SubElement(annotation, 'path')
#     path2.text = path + "\\" + newname

#     source = SubElement(annotation, 'source')
#     database = SubElement(source, 'database')
#     database.text = 'Unknown'

#     size = SubElement(annotation, 'size')
#     width = SubElement(size, 'width')
#     width.text = img_width
#     height = SubElement(size, 'height')
#     height.text = img_height
#     depth = SubElement(size, 'depth')
#     depth.text = 3

#     segment = SubElement(annotation, 'segment')
#     segment.text = '0'

#     ob = SubElement(annotation, 'object')
#     name = SubElement(ob, 'name')
#     name.text = label
#     pose = SubElement(ob, 'pose')
#     pose.text = 'Unspecified'
#     truncated = SubElement(ob, 'truncated')
#     truncated.text = 0
#     difficult = SubElement(ob, 'difficult')
#     difficult.text = 0

#     bndbox = SubElement(ob, 'bndbox')
#     xmin = SubElement(bndbox, 'xmin')
#     xmin.text = Xmin
#     ymin = SubElement(bndbox, 'ymin')
#     ymin.text = Ymin
#     xmax = SubElement(bndbox, 'xmax')
#     xmax.text = Xmax
#     ymax = SubElement(bndbox, 'ymax')
#     ymax.text = Ymax

#     ###xml_path = path + "\\" + filename[:len(filename) - 4] + "xml"
#     tree = ElementTree(annotation)
#     tree.write(xml_path, encoding='utf-8')
#     i = i+1
#     print(i)



if __name__ == '__main__':
	with open("./trainval.txt",'r') as infile:
		lines = infile.readlines()
		for line in lines:
			image_path="./JPEGImages/"+line.strip()+".jpg"	
			pkl_path="./Annotations/"+line.strip()+".pkl"	
			new_image_path="./trans_JPEGImages/"+"trans_"+line.strip()+".jpg"	
			xml_path="./trans_Annotations/"+"trans_"+line.strip()+".xml"	
			try:
				gen_transform_img_ann( image_path, pkl_path, new_image_path, xml_path )
			except:
				print(image_path+"\n")
				continue
