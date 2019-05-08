import xml.etree.ElementTree as ET
import os
import pickle
import numpy as np
# read the value of the node of the xml to variable



# count = 0
class_dict={"apple":0,"Apple":0, "banana":1, "orange":2, "pineapple":3, "cake":4, "pizza": 5, "pear":6, "bread":7, "strawberry":8, "pudding":9, "ice": 10, "mango":11,"macron": 12, "sandwich": 13, "peach":14}
##xml_path="E:/scene_data/20190413/xml/"

xml_path="/home-ex/tclitc/miniconda3/envs/tensorflow-axj/axjWorkspace/Tmp/data_augmentation_test_data/image"
for (path, dirs, files) in os.walk(xml_path):
	for filename in files:
		if ".jpg" not in filename:
			continue
		print(filename)
		file_path = path+"/"+filename
		print('-----------')
		print(file_path)
		#try:
			#print(file_path)	
		pkl_path = file_path.split(".")[0]+".pkl"
		print(pkl_path)
		#pkl_file = open(pkl_path,'w')	
		updateTree = ET.parse(file_path)
		root = updateTree.getroot()
		#if "A_" not in filename:
		#	continue
		temp=[]
		count = 0
		for i in root.findall('object'):
			names = i.find('name')
			#print(type(names))
			#print(names.text)		### here need to get a conversion
			label = float(class_dict[names.text])
			boundingbox = i.find('bndbox')
			xmin = boundingbox.find('xmin')
			xmin = float(xmin.text)
			ymin = boundingbox.find('ymin')
			ymin = float(ymin.text)
			xmax = boundingbox.find('xmax')
			xmax = float(xmax.text)
			ymax = boundingbox.find('ymax')
			ymax = float(ymax.text)
			temp.append(xmin)
			temp.append(ymin)
			temp.append(xmax)
			temp.append(ymax)
			temp.append(label)
			count = count + 1

			print(temp)


			#temp=[xmin, ymin, xmax, ymax, label]
		data = np.reshape(np.array(temp),(count,5))
		print(data)
		with open(pkl_path,'wb') as pkl_file:
			pickle.dump(data, pkl_file, pickle.HIGHEST_PROTOCOL)
			#pkl_file.close()
				#pickle.dump(temp, pkl_file, 0)
		#pkl_file.close()

			#if count < 1:
			#print("xmin:",xmin)
		#count = count + 1
		#names = root.findall('filename')
		