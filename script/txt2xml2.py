from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
classes=['bicycle','car','motorcycle','chair','bed','couch','tv',
         'cell phone','laptop','microwave','oven','refrigerator','hair drier']

files_path=[r'F:/baidu/coco_datasets/bbox/{}/'.format(classes[i]) for i in range(len(classes))]
for k in range(len(classes)):
    files=os.listdir(files_path[k])
    os.mkdir(r'F:/baidu/samples/{}/'.format(classes[k]))
    for j in range(len(files)):
        file_path = files_path[k] + files[j]
        with open(file_path,'r') as f:

        line=f.readline()
        row=line.split()

        annotation = Element('annotation')

        folder = SubElement(annotation, 'folder')
        folder.text = classes[k]

        filename2 = SubElement(annotation, 'filename')
        newname = files[j].split('.')[0]+'.jpg'
        filename2.text = newname

        path2 = SubElement(annotation, 'path')
        path2.text = newname

        source = SubElement(annotation, 'source')
        database = SubElement(source, 'database')
        database.text = 'Unknown'

        size = SubElement(annotation, 'size')
        width = SubElement(size, 'width')
        width.text = row[0]
        height = SubElement(size, 'height')
        height.text = row[1]
        depth = SubElement(size, 'depth')
        depth.text = str(3)

        segment = SubElement(annotation, 'segment')
        segment.text = '0'
        for i in range(int((len(row) - 2) / 4)):
            ob = SubElement(annotation, 'object')
            name = SubElement(ob, 'name')
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
        tree = ElementTree(annotation)
        tree.write(xml_path)
