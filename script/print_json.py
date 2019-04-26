import os
import shutil
import re
import time
import json
import xml.etree.ElementTree as ET


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


# {'60':'bread','69':'apple','74':'cake','108':'orange','109':'banana','131':'pizza','171':'strawberry','181':'pear','211':'mango','219':'ice','229':'pineapple','256':'sandwich','232':'peach'}

# {'bread','apple','cake','orange','banana','pizza','strawberry','pear','mango','ice','pineapple','sandwich','peach'}


# file_name_dict={'obj365_val_000000354609.jpg':[width,height,total,name,bbox,name,bbox]}

# 怎么保证id/width/height只有一份。

def solve(json_path, saved_xml_folder):
    need_categories_id = [60, 69, 74, 108, 109,
                          131, 171, 181, 211, 219, 229, 256, 232]
    need_name = ['bread', 'apple', 'cake', 'orange', 'banana', 'pizza',
                 'strawberry', 'pear', 'mango', 'ice cream', 'pine apple', 'sandwich', 'peach']
    file_name_dict = {}
    file_name_list = []
    previous_file_name = ""
    change = 0
    # open(saved_xml_list,'r')
    with open(json_path, 'r') as load_f:
        load_dict = json.load(load_f)
    # print(load_dict['images'][0])
    ############
    # annotations: {'image_id': 354609, 'area': 9945.156009311546, 'category_id': 21, 'id': 0, 'iscrowd': 0, 'bbox': [133.8088989172, 178.6294555648, 80.1972656534, 124.0086669824]}
    # categories: {'id': 224, 'name': 'scale'}
    # images: {'id': 354609, 'height': 512, 'file_name': 'obj365_val_000000354609.jpg', 'width': 683}
    # print(load_dict)
        length_annotations = len(load_dict['annotations'])
        length_images = len(load_dict['images'])
        length_categories = len(load_dict['categories'])
        count = 0
        for num in range(length_annotations):

            if load_dict['annotations'][num]['category_id'] in need_categories_id:
                # count = count + 1
                image_id = load_dict['annotations'][num]['image_id']
                category_id = load_dict['annotations'][num]['category_id']
                bbox = load_dict['annotations'][num]['bbox']

                for number_c in range(length_categories):
                    if category_id in load_dict['categories'][number_c].values():
                        name = load_dict['categories'][number_c]['name']
                    # else:
                        # name ='fucking'
                        # print(name)
                # 在images 里查询并获取file_name

                for number in range(length_images):

                    if image_id in load_dict['images'][number].values():
                        file_name = load_dict['images'][number]['file_name']
                        width = load_dict['images'][number]['width']
                        height = load_dict['images'][number]['height']
                        count_tmp = count
                        if file_name not in file_name_dict:
                            count = count + 1
                            # file_name_dict[file_name].append(image_id)
                            # print(type(file_name))
                            file_name_dict.setdefault(
                                file_name, []).append(width)
                            file_name_dict.setdefault(
                                file_name, []).append(height)
                            # file_name_dict.setdefault(file_name，[]).append(0)
                            next_file_name = file_name
                        # else:
                        if previous_file_name == "":
                            previous_file_name = file_name
                        if previous_file_name == file_name and num < length_annotations - 1:
                            change = 0
                        elif previous_file_name != file_name:
                            change = 1
                            anno_file_name = previous_file_name
                            previous_file_name = file_name  # border condition
                        else:  # final
                            change = 1
                            anno_file_name = previous_file_name
                        # file_name_dict[file_name][2] = file_name_dict[file_name][2] + 1
                        file_name_dict.setdefault(file_name, []).append(name)
                        file_name_dict.setdefault(file_name, []).append(bbox)

                        # print(anno_file_name)
                        # file_name_dict[anno_file_name]
                        # if file_name_dict.keys()=='obj365_val_000000646829.jpg':
                        #	print("fucking")
                        if change == 1:  # 将上一个存起来写入xml, 最后一个file_name怎么解决？
                            annotation = ET.Element('annotation')
                            folder = ET.SubElement(annotation, 'folder')
                            folder.text = 'voc2012'
                            filename2 = ET.SubElement(annotation, 'filename')
                            filename2.text = anno_file_name
                            source = ET.SubElement(annotation, 'source')
                            database = ET.SubElement(source, 'database')
                            database.text = 'Unknown'
                            size = ET.SubElement(annotation, 'size')
                            width = ET.SubElement(size, 'width')
                            # copy image

                            width.text = str(file_name_dict[anno_file_name][0])
                            height = ET.SubElement(size, 'height')
                            height.text = str(
                                file_name_dict[anno_file_name][1])
                            depth = ET.SubElement(size, 'depth')
                            depth.text = str(3)
                            segment = ET.SubElement(annotation, 'segment')
                            segment.text = '0'
                            length = len(file_name_dict[anno_file_name]) - 2
                            object_node = file_name_dict[anno_file_name]
                            for object_number in range(int(length/2)):

                                ob = ET.SubElement(annotation, 'object')
                                name = ET.SubElement(ob, 'name')
                                if object_node[2*object_number+2] == "pine apple":
                                    # name.text = object_node[2*object_number+2]
                                    name.text = "pineapple"

                                elif object_node[2*object_number+2] == "ice cream":
                                    name.text = "ice"
                                else:
                                    name.text = object_node[2*object_number+2]
                                pose = ET.SubElement(ob, 'pose')
                                pose.text = 'Unspecified'
                                truncated = ET.SubElement(ob, 'truncated')
                                truncated.text = '0'
                                difficult = ET.SubElement(ob, 'difficult')
                                difficult.text = '0'

                                bndbox = ET.SubElement(ob, 'bndbox')
                                xmin = ET.SubElement(bndbox, 'xmin')
                                # need to revise
                                xmin.text = str(
                                    int(object_node[2*object_number+1+2][0]))
                                ymin = ET.SubElement(bndbox, 'ymin')
                                # need to revise
                                ymin.text = str(
                                    int(object_node[2*object_number+1+2][1]))
                                xmax = ET.SubElement(bndbox, 'xmax')
                                # need to revise
                                xmax.text = str(
                                    int(object_node[2*object_number+1+2][0]+object_node[2*object_number+1+2][2]))
                                ymax = ET.SubElement(bndbox, 'ymax')
                                # need  to revise
                                ymax.text = str(
                                    int(object_node[2*object_number+1+2][1]+object_node[2*object_number+1+2][3]))
                            xml_path = saved_xml_folder + \
                                anno_file_name.split(
                                    '.')[0] + '.xml'  # need to revise
                            tree = ET.ElementTree(annotation)
                            tree.write(xml_path)
                            print("XML_Path:", xml_path)


def copy_file(xml_path, img_path, new_path):
	xml_n, xml_p = get_file_name_path(xml_path)
	jpg_n, jpg_p = get_file_name_path(img_path)

	for jp in jpg_p:

		jp_name = re.split('/', jp)
		jp_name = f_name[-1][:-4] + '.xml'

		if jp_name in xml_n:
			shutil.copy2(jp, new_path)
			print("Copy:", jp, "To:", new_path)
		else:
			print("Not Found:", jp)


#################################
if __name__ == '__main__':
	control == 1

    json_path = "../tmp/object365/train.json"
    saved_xml_folder = "../tmp/object365/use_data/train/annotation/"

    img_path = "../tmp/object365/images/Part/"
    save_img_path = "../tmp/object365/use_data/train/images/"
	if control == 0: 
    	solve(json_path, saved_xml_folder)
	else:
		copy_file(saved_xml_folder, img_path, save_img_path)
		


# obj365_val_000000190026.jpg
