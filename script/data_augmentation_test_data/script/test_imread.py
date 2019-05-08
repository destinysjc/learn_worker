import cv2
import xml.etree.ElementTree as ET


def read_image(jpg_path):
    jpg_path = '/home-ex/tclitc/miniconda3/envs/tensorflow-axj/axjWorkspace/Tmp/data_augmentation_test_data/image/apple/bz_apple_0.jpg'
    img = cv2.imread(jpg_path)
    print(img.shape)

# draw box bunding
def draw_box(jpg_path, xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    obj_n = root.findall("object/name")
    obj_xmin = root.findall("object/bndbox/xmin")
    obj_ymin = root.findall("object/bndbox/ymin")
    obj_xmax = root.findall("object/bndbox/xmax")
    obj_ymax = root.findall("object/bndbox/ymax")
    for i in range(len(obj_n)):
        ob_n = obj_n[i].text
        xmin = int(obj_xmin[i].text)
        ymin = int(obj_ymin[i].text)
        xmax = int(obj_xmax[i].text)
        ymax = int(obj_ymax[i].text)
        #print(ob_n.text)
        print(xmin)
        img = cv2.imread(jpg_path)
        #print(img)
        img = cv2.rectangle(img, (xmin, ymax), (xmax, ymin), (55,255,155), 4)
        #plt.imshow(img,'brg')
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(img, (ob_n), (xmin-2, ymax-1), font, 1, (3,3,255), 1)
        #cv2.putText(img, text, (212, 310), 2, (55,0,255), 1)
        cv2.imwrite(jpg_path, img)
        #     print(a_i['category_id'])
        # for a_i in ann_img[1:]:
        #     xmin = int(a_i['bbox'][0])
        
        #     ymin = int(a_i['bbox'][3])
        #     xmax = int(a_i['bbox'][2])
        #     ymax = int(a_i['bbox'][1])
        
        #     img = cv2.imread(jpg_path)
        #     img = cv2.rectangle(img, (xmin, ymax), (xmax, ymin), (55,255,155), 4)
        #     #plt.imshow(img,'brg')
        #     font = cv2.FONT_HERSHEY_COMPLEX
        #     cv2.putText(img, str(a_i['category_id']), (xmin-2, ymax-1), font, 1, (3,3,255), 1)
        #     #cv2.putText(img, text, (212, 310), 2, (55,0,255), 1)
        #     cv2.imwrite(jpg_path, img)
        #     print(a_i['category_id'])

def draw_boxs(jpg_path, xml_path):
    tree = ET.ElementTree(xml_path)
    #root = tree.getroot()
    
    for sub in tree.iter(tag='object'):
        print(sub.tag, sub.attrib, sub.text)

if __name__ == "__main__":
    xml_path = './mix_bz_pear_0.xml'
    jpg_path = './mix_bz_pear_0.jpg'
    save_path = "./test_0.jpg"
    draw_box(jpg_path, xml_path)