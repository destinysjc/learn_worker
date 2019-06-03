import os 
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


def judge_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    file_object = root.findall('object/name')
    # print(file_name.text)
    # print(file_size_w.tag, file_size_w.attrib, file_size_w.text)
    # print(file_size_h.tag, file_size_h.attrib, file_size_h.text)
    # print(file_size_d.tag, file_size_d.attrib, file_size_d.text)
    # print(file_segmented.tag, file_segmented.attrib, file_segmented.text)
    for fob in file_object:
        if fob.text == "plaque" or fob.text == "sclerosis":
            fob.text = "abnormal"
        elif fob.text == "pseudomorphism":
            fob.text = "noraml"

        print(fob.tag, fob.attrib, fob.text)
    tree.write(xml_path)
    print("修改文件：", xfp)

    
    
    # print("---------------")
    # for fn in root.iter("filename"):
    #     print(fn.text)


    # for r in root:
    #     file_name = r.findall('filename')
    #     file_source = r.findall('source')
    #     file_owner = r.findall('owner')
    #     file_size = r.findall('size')
    #     file_segmented = r.findall('segmented')
    #     file_object = r.findall('object/name')
    #     file_n = r.findall('object/n')
        
    #     print(r.tag, r.attrib, r.text, r.tail)
    #     print("----------------------")
    #     print(file_name)
    #     print("----------------------")
    #     print(file_source)
    #     print("----------------------")
    #     print(file_owner)
    #     print("----------------------")
    #     print(file_size)
    #     print("----------------------")
    #     print(file_segmented)
    #     print("----------------------")
    #     print(file_object)
    #     print("----------------------")
    #     print(file_n)


if __name__ == "__main__":
    xml_path = './image'
    xml_file_name, xml_file_path = get_file_name_path(xml_path, ".xml")
    for xfp in xml_file_path:

        judge_xml(xfp)
        