import os
import shutil
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
           
    return jpg_file_name, jpg_file_path


def remove_node(xml_path, key_map):
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    nodes = tree.findall(key_map)
    print(root.text)
    for i in nodes:
        n = i.findall('name')
        print(type(n))
        print(n)
        for n_ in n:
            if n_.text == 'normal':
                print(i)
                root.remove(i)
                tree.write(xml_path)
    # for node in root.iter(key_map):
    #     print(node.tag, node.attrib, node.text)
        
    #     if node.text == 'normal':
    #         root.remove(key_map)
    #     tree.write(xml_path)

def remove_file(file_path, keys):
    for fp in file_path:
        if '正常' in fp:
            shutil.rmtree(fp)



remove_node(r'C:\Users\Administrator\Desktop\learn_worker\Tmp\object365\000001.xml', 'object')