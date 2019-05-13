import os
import cv2
import time
import numpy as np
import tensorflow as tf
import xml.etree.ElementTree as ET
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID" 
os.environ['CUDA_VISIBLE_DEVICES'] = "2"
config = tf.ConfigProto() 
config.gpu_options.per_process_gpu_memory_fraction = 0.9 
session = tf.Session(config=config)


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

# batch test image and general *label.txt
class TOD(object):
    def __init__(self):
        self.PATH_TO_CKPT = "/home-ex/tclsz/liqiming/data/VOCdevkit/pb_model/frozen_inference_graph.pb"
        self.PATH_TO_LABELS = "/home-ex/tclsz/liqiming/data/VOCdevkit/scene_label_map.pbtxt"
        self.NUM_CLASSES = 17
        self.detection_graph = self._load_model()
        self.category_index = self._load_label_map()
        category_index = self.category_index
    def _load_model(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph

    def _load_label_map(self):
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index

    def detect(self, image_path, threshold):
        # image = cv2.imread(image_path)
        # size = image.shape
        result_list=[]
        jpg_file_name, jpg_file_path = get_file_name_path(image_path, format_key=".jpg")
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                
                #print(jpg_file_path)
                
                for fp, i in zip(jpg_file_path, range(len(jpg_file_path))):
                    #i = 0
                    txt_path = fp[:-4] + '.txt'
                    #print(txt_path)
                    txt_write = open(txt_path,'w')
                    image = cv2.imread(fp)
                    
                    size = np.shape(image)
                    #print(size)
                    image_np_expanded = np.expand_dims(image, axis=0)
                    image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                    boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                    # Actual detection.
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    ## Visualization of the results of a detection.
                    
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        self.category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)
                    txt_write.write(fp + " " + str(size[0]) + " " + str(size[1]) + " " + str(size[2]) + "\n")
                    for num in range(len(num_detections)):
                        py_scores = np.array(scores)[num]
                        py_classes = np.array(classes)[num]
                        py_boxes = np.array(boxes)[num]
                        #print(py_scores[0])
                
                        if py_scores[num] > threshold:
                            classes_ = int(py_classes[num])
                            classes_n = self.category_index[classes_]
                            classes_n = classes_n['name']
                            txt_write.write(str(classes_n + " "))
                            txt_write.write(str(py_boxes[num][0]) + " ")
                            txt_write.write(str(py_boxes[num][1]) + " ")
                            txt_write.write(str(py_boxes[num][2]) + " ")
                            txt_write.write(str(py_boxes[num][3]) + "\n")
                            result_list.append(fp)
                            result_list.append(py_scores[num])
                            result_list.append(py_classes[num])
                            result_list.append(py_boxes[num])
                            #print(type(self.category_index))
                            classes_ = int(py_classes[num])
                            classes_n = self.category_index[classes_]
                            classes_n = classes_n['name']
                            print(classes_n)
                    result_list.append(size)
                    txt_write.close()
                    
                    print('save %dst txt file: %s'%(i+ 1, txt_path))

# normalization class list:[[file_path, hieght, wight, deepth], [classes, xmin, ymin, xmax, ymax]]
def write_class_l(file_path):
    label_info = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        names = lines[0].split("\n")
        names = (names[0]).split()
        name = [names[0], int(names[1]), int(names[2]), int(names[3])]
        for line in lines[1:]:
            line = line.split()
            print(line[0])
            #label_info.pop(line[0])
            clas = [line[0]]
            li = list(map(float, line[1:]))
            cla = clas + li
            label_info.append(cla)
            
        label_info.append(name)
        print(label_info)
        print("-------------")
        return label_info
        
# write pascal Voc's *.xml     
def write_voc_xml(txt_path):
    
    label_info = write_class_l(txt_path)
    file_path = label_info[-1][0]
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
    width.text = str(label_info[-1][-2])
    height = ET.SubElement(size, 'height')
    height.text = str(label_info[-1][-3])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(label_info[-1][-1])

    segment = ET.SubElement(annotation, 'segment')
    segment.text = '0'
    
    for i in range(len(label_info)-1):
        
        ob = ET.SubElement(annotation, 'object')
        name = ET.SubElement(ob, 'name')
        name.text = str(label_info[i][0])
        pose = ET.SubElement(ob, 'pose')
        pose.text = 'Unspecified'
        truncated =ET.SubElement(ob, 'truncated')
        truncated.text = 0
        difficult = ET.SubElement(ob, 'difficult')
        difficult.text = 0

        bndbox = ET.SubElement(ob, 'bndbox')
        #print(label_info[i][1][0])
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(label_info[i][1] * label_info[-1][-2])
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(label_info[i][2] * label_info[-1][-3])
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(label_info[i][3] * label_info[-1][-2])
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(label_info[i][4] * label_info[-1][-3])

    xml_path = file_path = label_info[-1][0][:-4] + '.xml'
    
    tree = ET.ElementTree(annotation)
    tree.write(xml_path)
    

if __name__=="__main__":
    # batch detecion video slice image, general label.txt 
    path = "/home-ex/tclsz/anxiangjing/images/"
    threshold = 0.1
    detecotr = TOD()
    detecotr.detect(path, threshold)

    time.sleep(1)
    print('sleep 1s')
    # batch general label.xml
    xml_file_name, xml_file_path = get_file_name_path(path, format_key='.txt')
    for fp, i in zip(xml_file_path, range(len(xml_file_name))):
        write_voc_xml(fp)
       
        print('save %dst xml file: %s'%( i+1, fp[:-4] + '.xml'))
        
    print("Successful!!!")