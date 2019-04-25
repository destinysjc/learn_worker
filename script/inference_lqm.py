import os
import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID" 
os.environ['CUDA_VISIBLE_DEVICES'] = "3"
config = tf.ConfigProto() 
config.gpu_options.per_process_gpu_memory_fraction = 0.9 
session = tf.Session(config=config)





class TOD(object):
    def __init__(self):
        self.PATH_TO_CKPT = "/home-ex/tclsz/liqiming/data/VOCdevkit/pb_model/frozen_inference_graph.pb"
        self.PATH_TO_LABELS = "/home-ex/tclsz/liqiming/data/VOCdevkit/scene_label_map.pbtxt"
        self.NUM_CLASSES = 17
        self.detection_graph = self._load_model()
        self.category_index = self._load_label_map()

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
        image = cv2.imread(image_path)
        result_list=[]
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
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
                #vis_util.visualize_boxes_and_labels_on_image_array(
                #    image,
                #    np.squeeze(boxes),
                #    np.squeeze(classes).astype(np.int32),
                #    np.squeeze(scores),
                #    self.category_index,
                #    use_normalized_coordinates=True,
                #    line_thickness=8)
                for num in range(len(num_detections)):
                    py_scores = np.array(scores)[num]
                    py_classes = np.array(classes)[num]
                    py_boxes = np.array(boxes)[num]
                    #print(py_scores[0])
			
                    if py_scores[num] > threshold:
                    ### save the image and save the result
                        #print(py_scores[num])
                        result_list.append(image_path)
                        result_list.append(py_scores[num])
                        result_list.append(py_classes[num])
                        result_list.append(py_boxes[num])

        #cv2.namedWindow("detection", cv2.WINDOW_NORMAL)
        #cv2.imshow("detection", image)
        #cv2.waitKey(0)
        return result_list

if __name__ == '__main__':
    #input video for biaozhu;

    #
    result = open("./result.txt",'w')
    path = "./image.jpg"

    threshold = 0.1
    #image = cv2.imread('image.jpg')
    detecotr = TOD()
    result_list=detecotr.detect(path,threshold)
    print(result_list)
    print(len(result_list))
    print(type(result_list))

    length = int(len(result_list))/4
    length = int(length)
    if len(result_list) != 0:
        for num in range(length):
            result.write(result_list[num*4]+" ")
            result.write(str(result_list[4*num+1])+" ")
            result.write(str(result_list[4*num+2])+" ")
            result.write(str(result_list[4*num+3][0])+" ")
            result.write(str(result_list[4*num+3][1])+" ")
            result.write(str(result_list[4*num+3][2])+" ")
            result.write(str(result_list[4*num+3][3])+"\n")


    result.close()
