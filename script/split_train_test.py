import os
import shutil
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

def split_train_test(file_list):
    split_rate = ((len(file_list) // 10) // 3) * 3
    test_l = file_list[:split_rate]
    train_l = file_list[split_rate:]
    print(len(test_l))
    print(len(train_l))
    return test_l, train_l


def split_train_test_xml(file_list, jpg_list):
    xml_l = []
    for i in file_list:
        for j in jpg_list:
            if i[:-4] in j:
                xml_l.append(i)
    return xml_l


def copy_file(file_path, new_path):
    isExists=os.path.exists(new_path)
    if not isExists:
        os.makedirs(new_path)
    shutil.copy2(file_path, new_path)

if __name__ == "__main__":
    jpg_path = r'../workTrains/train_ssdlite/image/dataVoc/Wine'
    test_path = '../workTrains/train_ssdlite/image/test/'
    train_path = '../workTrains/train_ssdlite/image/train/'
    jpg_file_name, jpg_file_path = get_file_name_path(jpg_path, '.jpg')
    xml_file_name, xml_file_path = get_file_name_path(jpg_path, '.xml')

    jpg_test, jpg_train = split_train_test(jpg_file_path)
    xml_test = split_train_test_xml(xml_file_path, jpg_test)
    xml_train = split_train_test_xml(xml_file_path, jpg_train)
    
    for i, j in zip(jpg_test, xml_test):
        copy_file(i, test_path)
        copy_file(j, test_path)
        print('test data-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->' * 2)
        print('copy file: ', i, j, '-->', test_path)

    for i, j in zip(jpg_train, xml_train):
        copy_file(i, train_path)
        copy_file(j, train_path)
        print('train data-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->-->' * 2)
        print('copy file: ', i, j, '-->', train_path)