from data_aug.data_aug import *
# from data_aug.bbox_util import *
import cv2
import pickle as pkl
import numpy as np
import random
from xml.etree.ElementTree import SubElement, Element, ElementTree
# import matplotlib.pyplot as plt


# img = cv2.imread("messi.jpg") #OpenCV uses BGR channels
# bboxes = pkl.load(open("messi_ann.pkl", "rb"))

# print(bboxes)
# vice_bboxes = bboxes
# vice_bboxes=  vice_bboxes.tolist()

# print(type(vice_bboxes))
# print(vice_bboxes)

# new_bboxes = vice_bboxes + bboxes


# print(new_bboxes)


# transforms = Sequence([RandomHorizontalFlip(1), RandomScale(0.2, diff = True), RandomRotate(10)])


# mixup
def mixup2images(src1, src2, alpha):

    # src1 = "E:/DataAugmentationForObjectDetection-master/DataAugmentationForObjectDetection-master/b_pizza_103.jpg"

    # src2 = "E:/DataAugmentationForObjectDetection-master/DataAugmentationForObjectDetection-master/messi.jpg"

    mixup = Mixup(src1, src2, alpha)
    img, bboxes = mixup.process()
    return img, bboxes
    # transforms = Sequence(Mixup(0.3))

    # img, bboxes = transforms(src1, src2)

    # cv2.imwrite("liqiming_mixup.jpg",img)
# print(bboxes)
# plt.imshow(draw_rect(img, bboxes))


if __name__ == '__main__':
    class_dict={0:"apple", 1:"banana", 2:"orange", 3:"pineapple", 4:"cake", 5: "pizza", 6:"pear", 7:"bread", 8:"strawberry", 9:"pudding",  10:"ice", 11:"mango",12: "macron", 13: "sandwich", 14:"peach"}
    image_apple_path = "/home-ex/tclitc/miniconda3/envs/tensorflow-axj/axjWorkspace/Tmp/data_augmentation_test_data/image/apple/bz_apple_21.jpg"
    image_pear_list = "./images_pear.list"
    # lines = []
    with open(image_pear_list, 'r') as infile:
        lines = infile.readlines()

    length = len(lines)

    for num in range(length):

        # 这两行需不需要加".jpg" 以及 ".xml"，根据image.list的内容来。
        # image_list是图像列表，格式可能如下所示(所用是绝对路径)：
        '''
        /home/data/image1.jpg
        /home/data/image2.jpg
        /home/data/image3.jpg
        /home/data/image4.jpg
        /home/data/image5.jpg
        /home/data/image6.jpg
        /home/data/image6.jpg
        '''
        base_image_name = lines[num].strip().split('/')[-1].split('.')[0]
        out_image_path = "./trans_JPEGImages/"+"mix_"+base_image_name+".jpg"
        out_xml_path = "./trans_Annotations/"+"mix_"+base_image_name+".xml"

        src1 = lines[num].strip()
        # if '\n' in src1:
        #     print("fucking you")

        # print("-------")
        # print(src1)
        # print("-------")

        random_number = random.uniform(num+1, length - 1)
        random_number = int(random_number)

        #src2 = lines[random_number].strip()
        src2 = image_apple_path

        alpha = random.uniform(0.1, 0.9)
        #print(src1, "--->", src2)
        img, bboxes = mixup2images(src1, src2, alpha)

        # print(img)
        # save the image and bounding box
        # save pkl_file
        # pkl_file =
        # with open(pkl_path,'wb') as pkl_file:
        # 	pickle.dump(data, pkl_file, pickle.HIGHEST_PROTOCOL)

        # save the output xml file
        row, col = bboxes.shape
        img_height, img_width, channels = img.shape

        annotation = Element('annotation')

        folder = SubElement(annotation, 'folder')
        folder.text = "label"

        filename2 = SubElement(annotation, 'filename')
        filename2.text = "mix_"+base_image_name+".jpg"

        path2 = SubElement(annotation, 'path')
        path2.text = "./trans_JPEGImages/"+"mix_"+base_image_name+".jpg"

        source = SubElement(annotation, 'source')
        database = SubElement(source, 'database')
        database.text = 'Unknown'

        size = SubElement(annotation, 'size')
        width = SubElement(size, 'width')
        width.text = str(img_width)
        height = SubElement(size, 'height')
        height.text = str(img_height)
        depth = SubElement(size, 'depth')
        depth.text = "3"

        segment = SubElement(annotation, 'segment')
        segment.text = '0'

        for Row in range(row):
            ob = SubElement(annotation, 'object')
            name = SubElement(ob, 'name')
        # name.text = str(bboxes[Row][4])
            name.text = str(class_dict[(int(bboxes[Row][4]))])
            pose = SubElement(ob, 'pose')
            pose.text = 'Unspecified'
            truncated = SubElement(ob, 'truncated')
            truncated.text = '0'
            difficult = SubElement(ob, 'difficult')
            difficult.text = '0'

            bndbox = SubElement(ob, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(int(bboxes[Row][0]))
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(int(bboxes[Row][1]))
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(int(bboxes[Row][2]))
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(int(bboxes[Row][3]))
        tree = ElementTree(annotation)
        tree.write(out_xml_path, encoding='utf-8')
        

        # end of save the output xml file

        # save the output img file

        cv2.imwrite(out_image_path, img)
        print('Writing XML:',out_xml_path)
        print('Writing Image:',out_image_path)
