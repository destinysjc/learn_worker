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



def write_class_txt(file_path):
    result = open("./results.txt",'w')
    with open(file_path, 'r') as f:
        lines = f.readlines()
        names = lines[0].split(" ")
        print(names)
        result.write(names[0] + '\n')
        new_txt = [names[0], float(names[2])]
        for line in lines:
            line = line.split()
            #print(line)
            result.write(line[2] + ' ')
            result.write(line[3] + ' ')
            result.write(line[4] + ' ')
            result.write(line[5] + ' ')
            result.write(line[6] + '\n')
            
            #new_txt.append(line[2])
            new_txt.append(float(line[3]))
            new_txt.append(float(line[4]))
            new_txt.append(float(line[5]))
            new_txt.append(float(line[6]))
        result.close()
        print("-------------")
        print(new_txt)


                
    

def write_voc_xml(txt_path):


    file_path = txt_path[-4] + '.xml'
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
            pose = ET.SubElement(ob, 'pose')
            pose.text = 'Unspecified'
            truncated =ET.SubElement(ob, 'truncated')
            truncated.text = 0
            difficult = ET.SubElement(ob, 'difficult')
            difficult.text = 0

            bndbox = ET.SubElement(ob, 'bndbox')

            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = str(round(float(row[2+4*i])))
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = ET.str(round(float(row[3+4*i])))
            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = str(round(float(row[4+4*i])))
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = str(round(float(row[5+4*i])))

        xml_path = r'F:/baidu/samples/{}/'.format(classes[k])+files[j].split('.')[0]+ ".xml"
        tree = ET.ElementTree(annotation)
        tree.write(xml_path)

if __name__ == "__main__":
    txt_path = './result.txt'
    write_class_txt(txt_path)

