import cv2
import os

 
vc = cv2.VideoCapture(0) 
c = 1
 
 
if vc.isOpened():
 
    rval,frame = vc.read()
else:
    rval = False
 
timeF = 45 
save_path = r'C:/Users/Administrator/Desktop/learn_worker/Tmp/Captures/Mango/'

while rval:
    rval, frame = vc.read()
    if os.path.exists(save_path +'sb_'+str(c)+'.jpg') == True:
            print("skiping:", save_path +'sb_'+str(c)+'.jpg')
    else:
        if (c%timeF == 0):
            cv2.imwrite(save_path +'sb_'+str(c)+'.jpg',frame) 
            print("==Save:==",save_path +'sb_'+str(c)+'.jpg')
    c = c + 1
    key = cv2.waitKey(1)
    if key == ord('q'):
    	break
    elif key == ord(' '):
    	waitKey(0)
vc.release()
