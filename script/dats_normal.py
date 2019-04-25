import os
import csv
import numpy as np 
import xml.etree.ElementTree as ET

# get file_name, file_path
def get_file_name_path(dir_file):
    jpg_file_name = []
    jpg_file_path = []
    xml_file_name = []
    xml_file_path = []
    for root, dirs, files in os.walk(dir_file):
        for f in files:
            if '.jpg' in f:
                jpg_file_name.append(f)
                jpg_file_path.append(os.path.join(root, f))
            elif '.xml' in f:
                xml_file_name.append(f)
                xml_file_path.append(os.path.join(root, f))

    return jpg_file_name, jpg_file_path, xml_file_name, xml_file_path



def get_class_list(file_path, size, classes, boxes):
    info_list = [file_path, size, classes, boxes]
    if 
    return info_list

# def get_info_list():
#     for i in 
# write .xml format
def write_voc_xml(xml_info, ):

    file_path = xml_info[0][-4] + '.xml'
    with open(file_path,'r') as f:
        #i=0
        line=f.readline()
        row=line.split()

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
        width.text = xml_info[1][0]
        height = ET.SubElement(size, 'height')
        height.text = xml_info[1][1]
        depth = ET.SubElement(size, 'depth')
        depth.text = xml_info[1][1]

        segment = ET.SubElement(annotation, 'segment')
        segment.text = '0'
        for i in range(int((len(row) - 2) / 4)):
            ob = ET.SubElement(annotation, 'object')
            name = ET.SubElement(ob, 'name')
            name.text = classes[k]
            pose = SubElement(ob, 'pose')
            pose.text = 'Unspecified'
            truncated = SubElement(ob, 'truncated')
            truncated.text = 0
            difficult = SubElement(ob, 'difficult')
            difficult.text = 0

            bndbox = SubElement(ob, 'bndbox')

            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(round(float(row[2+4*i])))
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(round(float(row[3+4*i])))
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(round(float(row[4+4*i])))
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(round(float(row[5+4*i])))

        xml_path = r'F:/baidu/samples/{}/'.format(classes[k])+files[j].split('.')[0]+ ".xml"
        tree = ET.ElementTree(annotation)
        tree.write(xml_path)



