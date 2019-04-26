import os
import csv
import re
import json
import cv2
import shutil
import time
#import matplotlib.pyplt as plt
import numpy as np 
import xml.etree.ElementTree as ET


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





def find_label_map(json_path, file_name, labels):
    with open(json_path) as f:
        
        json_dict = json.load(f)
        json_img = json_dict['images']
        json_ann = json_dict['annotations']
        
        for js_img in json_img:
            if js_img['file_name'] == file_name:
                for js_ann in json_ann:
                    if js_img['id'] == js_ann['image_id'] :
                        js_label = js_ann['category_id']
                        labels_map = {js_label:labels}
                        print(labels_map)

def label_map():
    label_map_dict = {'60':'bread','69':'apple','74':'cake','108':'orange','109':'banana',
    '131':'pizza','171':'strawberry','181':'pear','211':'mango','219':'ice',
    '229':'pineapple','256':'sandwich','232':'peach'}
    return label_map_dict

def write_js_xml(json_path, save_path):
    label_map_dict = label_map()
    with open(json_path) as f:
        
        json_dict = json.load(f)
        json_img = json_dict['images']
        json_ann = json_dict['annotations']
        # del json_ann['area'] 
        # del json_ann['id'] 
        # del json_ann['iscrowd']

        for im in json_img:
            print('---1 for-----')
            start = time.time()
            for k in label_map_dict.keys():
                print('---2 for-----')
                i = 0
                for an in json_ann:
                    print('---3 for-----')
                    if (im['id'] == an['image_id']) and  (an['category_id'] == k):
                        print('---1 if-----')
                        if i<1:
                            print('---2 if-----')
                            annotation =ET.Element('annotation')

                            folder = ET.SubElement(annotation, 'folder')
                            folder.text = 'voc2012'

                            filename2 = ET.SubElement(annotation, 'filename')
                            filename2.text = im['file_name']


                            source = ET.SubElement(annotation, 'source')
                            database = ET.SubElement(source, 'database')
                            database.text = 'Unknown'

                            size = ET.SubElement(annotation, 'size')
                            width = ET.SubElement(size, 'width')
                            width.text = str(im['width'])
                            height = ET.SubElement(size, 'height')
                            height.text = str(im['height'])
                            depth = ET.SubElement(size, 'depth')
                            depth.text = str(3)

                            segment = ET.SubElement(annotation, 'segment')
                            segment.text = '0'
                            i+=1
                        else:
                            print('---3 if-----')
                            ob = ET.SubElement(annotation, 'object')
                            name = ET.SubElement(ob, 'name')
                            an_ = an['category_id']
                            classes = label_map_dict[an_]
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
                            xmin.text = str(an['bbox'][0])
                            ymin = ET.SubElement(bndbox, 'ymin')
                            ymin.text = str(an['bbox'][3])
                            xmax = ET.SubElement(bndbox, 'xmax')
                            xmax.text = str(an['bbox'][2])
                            ymax = ET.SubElement(bndbox, 'ymax')
                            ymax.text = str(an['bbox'][1])
                            xml_path = save_path + im['file_name'] + '.xml'
                            print('Useing Time:', int(time.time() - start),'-->Save path:', xml_path)
                            tree = ET.ElementTree(annotation)
                            tree.write(xml_path)
                            




 # generate *.xml
def write_json_xml(json_path, img_path, save_path):

    label_map_dict = label_map()
    with open(json_path) as f:
    
        json_dict = json.load(f)
        json_img = json_dict['images']
        json_ann = json_dict['annotations']
        
        start = time.time()
        for js_img in json_img:
    
            for js_ann in json_ann:
                if js_img['id'] == js_ann['image_id'] and js_ann['category_id'] in label_map_dict.keys():
                    ann_img.append(js_ann)
                    #print(ann_img)
                    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
                    shutil.copy2(img_path + js_img['file_name'], save_path)
                    l_map = js_ann['category_id']
                    annotation =ET.Element('annotation')

                    folder = ET.SubElement(annotation, 'folder')
                    folder.text = 'voc2012'

                    filename2 = ET.SubElement(annotation, 'filename')
                    filename2.text = js_img['file_name']


                    source = ET.SubElement(annotation, 'source')
                    database = ET.SubElement(source, 'database')
                    database.text = 'Unknown'

                    size = ET.SubElement(annotation, 'size')
                    width = ET.SubElement(size, 'width')
                    width.text = str(js_img['width'])
                    height = ET.SubElement(size, 'height')
                    height.text = str(js_img['height'])
                    depth = ET.SubElement(size, 'depth')
                    depth.text = str(3)

                    segment = ET.SubElement(annotation, 'segment')
                    segment.text = '0'

                    for a_i in ann_img:
                        obj_name = label_map_dict[a_i['category_id']]
                        ob = ET.SubElement(annotation, 'object')
                        name = ET.SubElement(ob, 'name')
                        name.text = str(obj_name)
                        pose = ET.SubElement(ob, 'pose')
                        pose.text = 'Unspecified'
                        truncated =ET.SubElement(ob, 'truncated')
                        truncated.text = 0
                        difficult = ET.SubElement(ob, 'difficult')
                        difficult.text = 0

                        bndbox = ET.SubElement(ob, 'bndbox')
                        #print(label_info[2][i])
                        xmin = ET.SubElement(bndbox, 'xmin')
                        xmin.text = str(a_i['bbox'][0])
                        ymin = ET.SubElement(bndbox, 'ymin')
                        ymin.text = str(a_i['bbox'][3])
                        xmax = ET.SubElement(bndbox, 'xmax')
                        xmax.text = str(a_i['bbox'][2])
                        ymax = ET.SubElement(bndbox, 'ymax')
                        ymax.text = str(a_i['bbox'][1])
                        #print(txt_path[-4])
            xml_path = save_path + js_img['file_name'] + '.xml'
            print('Useing Time:', int(time.time() - start),'-->Save path:', xml_path)
            tree = ET.ElementTree(annotation)
            tree.write(xml_path)

                    # if js_ann['category_id'] in label_map_dict.keys():
                    #     obj_name = label_map_dict[js_ann['category_id']]
                    #     ob = ET.SubElement(annotation, 'object')
                    #     name = ET.SubElement(ob, 'name')
                    #     name.text = str(obj_name)
                    #     pose = ET.SubElement(ob, 'pose')
                    #     pose.text = 'Unspecified'
                    #     truncated =ET.SubElement(ob, 'truncated')
                    #     truncated.text = 0
                    #     difficult = ET.SubElement(ob, 'difficult')
                    #     difficult.text = 0

                    #     bndbox = ET.SubElement(ob, 'bndbox')
                    #     #print(label_info[2][i])
                    #     xmin = ET.SubElement(bndbox, 'xmin')
                    #     xmin.text = str(js_ann['bbox'][0])
                    #     ymin = ET.SubElement(bndbox, 'ymin')
                    #     ymin.text = str(js_ann['bbox'][3])
                    #     xmax = ET.SubElement(bndbox, 'xmax')
                    #     xmax.text = str(js_ann['bbox'][2])
                    #     ymax = ET.SubElement(bndbox, 'ymax')
                    #     ymax.text = str(js_ann['bbox'][1])
                    #     #print(txt_path[-4])
                    #     xml_path = save_path + js_img['file_name'] + '.xml'
                    #     print('Useing Time:', int(time.time() - start),'-->Save path:', xml_path)
                    #     tree = ET.ElementTree(annotation)
                    #     tree.write(xml_path)    

        
# generate *.xml
def write_voc_xml(json_path, img_info, ann_info, img_path, save_path):
    #ann_img = load_json(json_path)
    start = time.time()
    label_map_dict = label_map()
    annotation =ET.Element('annotation')

    folder = ET.SubElement(annotation, 'folder')
    folder.text = 'voc2012'

    filename2 = ET.SubElement(annotation, 'filename')
    filename2.text = img_info['filename']


    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database')
    database.text = 'Unknown'

    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(img_info['width'])
    height = ET.SubElement(size, 'height')
    height.text = str(img_info['height'])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(3)

    segment = ET.SubElement(annotation, 'segment')
    segment.text = '0'
    for a_i in ann_info:
        ob = ET.SubElement(annotation, 'object')
        name = ET.SubElement(ob, 'name')
        for key, value in label_map_dict.items():
            while key == a_i['category_id']:

                name.text = str(value)
                pose = ET.SubElement(ob, 'pose')
                pose.text = 'Unspecified'
                truncated =ET.SubElement(ob, 'truncated')
                truncated.text = 0
                difficult = ET.SubElement(ob, 'difficult')
                difficult.text = 0

                bndbox = ET.SubElement(ob, 'bndbox')
                #print(label_info[2][i])
                xmin = ET.SubElement(bndbox, 'xmin')
                xmin.text = str(a_i['bbox'][0])
                ymin = ET.SubElement(bndbox, 'ymin')
                ymin.text = str(a_i['bbox'][3])
                xmax = ET.SubElement(bndbox, 'xmax')
                xmax.text = str(a_i['bbox'][2])
                ymax = ET.SubElement(bndbox, 'ymax')
                ymax.text = str(a_i['bbox'][1])
    #print(txt_path[-4])
    xml_path = '../tmp/object365/use_data/' + img_info['filename'] + '.xml'
    print('Useing Time:', int(time.time() - start),'-->Save path:', xml_path)
    tree = ET.ElementTree(annotation)
    tree.write(xml_path)

def write_img_xml(img_info, img_path, save_path):
    #ann_img = load_json(json_path)
    start = time.time()
    
    annotation =ET.Element('annotation')

    folder = ET.SubElement(annotation, 'folder')
    folder.text = 'voc2012'

    filename2 = ET.SubElement(annotation, 'filename')
    filename2.text = img_info['filename']


    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database')
    database.text = 'Unknown'

    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(img_info['width'])
    height = ET.SubElement(size, 'height')
    height.text = str(img_info['height'])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(3)

    segment = ET.SubElement(annotation, 'segment')
    segment.text = '0'
    
    #print(txt_path[-4])
    return annotation

def write_ann_xml(annotation, a_i, classes, save_path):
    label_map_dict = label_map()  
    #annotation =ET.Element('annotation')
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
    xmin.text = str(a_i['bbox'][0])
    ymin = ET.SubElement(bndbox, 'ymin')
    ymin.text = str(a_i['bbox'][3])
    xmax = ET.SubElement(bndbox, 'xmax')
    xmax.text = str(a_i['bbox'][2])
    ymax = ET.SubElement(bndbox, 'ymax')
    ymax.text = str(a_i['bbox'][1])
    return annotation
# draw box bunding
def draw_box(jpg_path, file_name):
    with open(json_path) as f:
        
        json_dict = json.load(f)
        json_img = json_dict['images']
        json_ann = json_dict['annotations']
        #ann_img = []
        for js_img in json_img:
            if js_img['file_name'] == file_name:
                ann_img = [js_img]
                print(ann_img)
                for js_ann in json_ann:
                    if js_img['id'] == js_ann['image_id'] :
                        ann_img.append(js_ann)
                        
                        print(js_ann)
                        print(ann_img)
            #print(ann_img)
        for a_i in ann_img[1:]:
            xmin = int(a_i['bbox'][0])
        
            ymin = int(a_i['bbox'][3])
            xmax = int(a_i['bbox'][2])
            ymax = int(a_i['bbox'][1])
        
            img = cv2.imread(jpg_path)
            img = cv2.rectangle(img, (xmin, ymax), (xmax, ymin), (55,255,155), 4)
            #plt.imshow(img,'brg')
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(img, str(a_i['category_id']), (xmin-2, ymax-1), font, 1, (3,3,255), 1)
            #cv2.putText(img, text, (212, 310), 2, (55,0,255), 1)
            cv2.imwrite(jpg_path, img)
            print(a_i['category_id'])


if __name__ == "__main__":
    json_path = '../tmp/object365/train.json'
    #load_json(json_path)

    # file_name = 'obj365_train_000000654374.jpg'
    # labels = 'apple'
    # find_label_map(json_path, file_name, labels)

    # file_name = 'obj365_train_000000664538.jpg'
    # labels = 'banana'
    # find_label_map(json_path, file_name, labels)

    # file_name = 'obj365_train_000000720638.jpg'
    # labels = 'strawberry'
    # find_label_map(json_path, file_name, labels)

    # file_name = 'obj365_train_000000074258.jpg'
    # labels = 'orange'
    # find_label_map(json_path, file_name, labels)

    # file_name = 'obj365_train_000000114098.jpg'
    # labels = 'ice cream'
    # find_label_map(json_path, file_name, labels)

    # file_name = 'obj365_train_000000677750.jpg'
    # labels = 'pizza'
    # find_label_map(json_path, file_name, labels)

    # file_name = 'obj365_train_000000087206.jpg'
    # labels = 'bread'
    # find_label_map(json_path, file_name, labels)

    # jpg_path = './tmp/obj365_train_000000720638.jpg'
    # f_ = re.split('/', jpg_path)
    # file_name = f_[-1]
    # #load_json(json_path)
    # draw_box(jpg_path, file_name)


    # img_path = '../tmp/object365/images/Part'
    # save_path = '../tmp/object365/use_data'
    # write_json_xml(json_path, img_path, save_path)

    # img_path = '../tmp/object365/images/Part'
    # save_path = '../tmp/object365/use_data'
    # json_info = load_json(json_path)
    # label_map_dict = label_map()
    # for js_info in json_info:
    #     start = time.time()
    #     for k in label_map_dict.keys():

    #         if k in js_info[1:]['category_id']:
    #             annotation = write_img_xml(js_info[0], img_path, save_path)
    #             shutil.copy2(img_path + js_info['file_name'], save_path)
    #             for ann in js_info[1:]:
    #                 classes_ = ann['category_id']
    #                 classes = label_map_dict[classes_]
    #                 annotation = write_ann_xml(annotation,ann, classes, save_path)

    #             xml_path = '../tmp/object365/use_data/' + js_info['file_name'] + '.xml'
    #             print('Useing Time:', int(time.time() - start),'-->Save path:', xml_path)
    #             tree = ET.ElementTree(annotation)
    #             tree.write(xml_path)
    save_path = '../tmp/object365/use_data'
    write_js_xml(json_path, save_path)



    
