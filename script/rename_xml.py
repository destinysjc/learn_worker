
# -*- coding: UTF-8 -*-

import os
#from xml.etree import ElementTree
 
 

###folder=["apple", "banana", "bread", "cake", "ice_cream", "macron","mango","orange","peach","pear","pizza","pudding","sandwich","strawberry"]#, "lawn", "plant", "plant_duorou"]



###########################folder=["apple", "banana"]###, "bread", "cake", "ice_cream", "macron","mango","orange","peach","pear","pizza","pudding","sandwich","strawberry"]#, "lawn", "plant", "plant_duorou"]

folder=["strawberry"]#, "lawn", "plant", "plant_duorou"]



######folder=["baby-car", "cake", "camera", "computer", "laptop", "lianyiqun"]#, "lawn", "plant", "plant_duorou"]
for m in range(0,len(folder)):
    root_dir = "D:/标注/strawberry(2002)/"
    file_list = os.listdir(root_dir)
    count = 2002
    for i in range(0, len(file_list)):
        path = root_dir + file_list[i]
        print(path)
        # #print(os.path.dirname(path)+"/"+"bijini"+"_"+str(i)+".jpg")
        os.rename(path,os.path.dirname(path)+"/"+"single_strawberry_"+str(count)+".jpg")
        print(os.path.dirname(path)+"/"+"single_strawberry_"+str(count)+".jpg")
        count = count + 1
