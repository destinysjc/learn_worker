
# -*- coding: UTF-8 -*-

import os
#from xml.etree import ElementTree
 
 

###folder=["apple", "banana", "bread", "cake", "ice_cream", "macron","mango","orange","peach","pear","pizza","pudding","sandwich","strawberry"]#, "lawn", "plant", "plant_duorou"]



###########################folder=["apple", "banana"]###, "bread", "cake", "ice_cream", "macron","mango","orange","peach","pear","pizza","pudding","sandwich","strawberry"]#, "lawn", "plant", "plant_duorou"]

folder=["mango"]#, "lawn", "plant", "plant_duorou"]



######folder=["baby-car", "cake", "camera", "computer", "laptop", "lianyiqun"]#, "lawn", "plant", "plant_duorou"]
for m in range(0,len(folder)):
    root_dir = "C:/Users/Administrator/Desktop/learn_worker/Tmp/Captures/mango/images/"
    file_list = os.listdir(root_dir)
    count = 413
    for i in range(0, len(file_list)):
        path = root_dir + file_list[i]
        print(path)
        # #print(os.path.dirname(path)+"/"+"bijini"+"_"+str(i)+".jpg")
        os.rename(path,os.path.dirname(path)+"/"+"a_mango_"+str(count)+".jpg")
        count = count + 1
