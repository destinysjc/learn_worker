import cv2
import os
def save_img():
    #video_path = r'D:\python3-PycharmProjects1\video2picture\20180911-12-48-31\data\123/'
    video_path = "/home-ex/tclitc/miniconda3/envs/tensorflow-axj/axjWorkspace/Tmp/strawberry/" 
    videos = os.listdir(video_path)
    print(videos)
    for video_name in videos:
        print(video_name)
        file_name = video_name.split('.')[0]
        folder_name =  file_name
        print(folder_name)
        os.makedirs(folder_name,exist_ok=True)
        vc = cv2.VideoCapture(video_path+video_name) # read the video file
        c = 1
        if vc.isOpened():  # tell if the video is open formally?
            rval, frame = vc.read()
        else:
            rval = False
 
        timeF = 12  
 
        while rval: # xun huan read video 
            rval, frame = vc.read()
            pic_path = folder_name + '/'
            if (c % timeF == 0):  # mei ge timeF zhen jin xing cun cu
                cv2.imwrite(pic_path + file_name + '_' + str(c) + '_' + 'strawberry' + '.jpg', frame)  # save as image, the name is foldername_number(di ji ge wen jian).jpg
                #cv2.imwrite(pic_path + file_name + '_' + str(c) + '.jpg', frame)
                print(pic_path + file_name + '_' + str(c) + '_' + 'strawberry' + '.jpg')  # save as image, the name is foldername_number(di ji ge wen jian).jpg
            c = c + 1
            cv2.waitKey(1)
        vc.release()
save_img()
