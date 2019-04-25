import json


#{'60':'bread','69':'apple','74':'cake','108':'orange','109':'banana','131':'pizza','171':'strawberry','181':'pear','211':'mango','219':'ice','229':'pineapple','256':'sandwich','232':'peach'}
need_categories_id=[60,69,74,108,109,131,171,181,211,219,229,256,232]

object_node=[]
anno_file_name=""
anno_foler_name=""
anno_path=""
anno_width=0
anno_height=0
anno_depth=3
with open("./val.json",'r') as load_f:
	load_dict = json.load(load_f)
	##################print(load_dict['images'][0])
	############
	#annotations: {'image_id': 354609, 'area': 9945.156009311546, 'category_id': 21, 'id': 0, 'iscrowd': 0, 'bbox': [133.8088989172, 178.6294555648, 80.1972656534, 124.0086669824]}
	#categories: {'id': 224, 'name': 'scale'}
	#images: {'id': 354609, 'height': 512, 'file_name': 'obj365_val_000000354609.jpg', 'width': 683}
	# print(load_dict)
	length_annotations = len(load_dict['annotations'])
	length_images = len(load_dict['images'])
	length_categories = len(load_dict['categories'])
	count = 0
	for num in range(length_annotations):
	 	if load_dict['annotations'][num]['category_id'] in need_categories_id:
	 		count = count + 1
	 		image_id = load_dict['annotations'][num]['image_id']
	 		category_id = load_dict['annotations'][num]['category_id']
	 		bbox = load_dict['annotations'][num]['bbox']
	 		for number in range(length_categories):
	 			if category_id in load_dict['categories'][number].values():
	 				name = load_dict['categories'][number]['name']
	 		for number in range(length_images):
	 			file_name = load_dict['images'][number]['file_name']
	 			width = load_dict['images'][number]['width']
	 			height = load_dict['images'][number]['height']
	 			if image_id in load_dict['images'][number].values():		## find the image_id in images
	 				if preview_file_name == file_name or count == 1:
	 					### 
	 					object_node.append(name)
	 					object_node.append(bbox)
	 					anno_file_name = file_name
	 					anno_width = width
	 					anno_height = height
	 				else:
	 					## write the annotation to the xml file and clear the object_node
	 					annotation =ET.Element('annotation')

						folder = ET.SubElement(annotation, 'folder')
						folder.text = 'voc2012'

						filename2 = ET.SubElement(annotation, 'filename')
						filename2.text = anno_file_name


						source = ET.SubElement(annotation, 'source')
						database = ET.SubElement(source, 'database')
						database.text = 'Unknown'

						size = ET.SubElement(annotation, 'size')
						width = ET.SubElement(size, 'width')
						width.text = anno_width
						height = ET.SubElement(size, 'height')
						height.text = anno_height
						depth = ET.SubElement(size, 'depth')
						depth.text = str(3)

						segment = ET.SubElement(annotation, 'segment')
						segment.text = '0'
	 					for object_number in range(len(object_node)/2):
	 						ob = ET.SubElement(annotation, 'object')
							name = ET.SubElement(ob, 'name')
							name.text = object_node[2*object_number]
							pose = ET.SubElement(ob, 'pose')
							pose.text = 'Unspecified'
							truncated =ET.SubElement(ob, 'truncated')
							truncated.text = 0
							difficult = ET.SubElement(ob, 'difficult')
							difficult.text = 0

							bndbox = ET.SubElement(ob, 'bndbox')
        #print(label_info[2][i])
							xmin = ET.SubElement(bndbox, 'xmin')
							xmin.text = object_node[2*object_number+1][]		### need to revise
							ymin = ET.SubElement(bndbox, 'ymin')
							ymin.text = object_node[2*object_number+1][]		### need to revise
							xmax = ET.SubElement(bndbox, 'xmax')
							xmax.text = object_node[2*object_number+1][]		### need to revise
							ymax = ET.SubElement(bndbox, 'ymax')
							ymax.text = object_node[2*object_number+1][]		### need  to revise

						xml_path = txt_path[:-4] + '.xml'						### need to revise
    					#print(xml_path)
    					tree = ET.ElementTree(annotation)
    					tree.write(xml_path)


    					##### 
    					object_node=[]


	 				preview_file_name = file_name   # 更新file_name

	 			#males = filter(lambda x:image_id== x[1], load_dict['images'][number].items())

	 		







#################################


