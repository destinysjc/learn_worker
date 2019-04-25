import cv2
import numpy as np
import os
import shutil
import time

def main():
    start=time.time()
    imgs=[]
    files=os.listdir(path)
    for i in range(len(files)):
        img_path=path+files[i]
        img=cv2.imread(img_path)
        img=cv2.resize(img,(size,size))
        img=np.array(img, np.float32) / 255
        imgs.append(img)

    i=0
    while i<len(imgs):
        j=i+1
        index=[]
        while j<len(imgs):

            diff=(imgs[i]-imgs[j])**2
            score = np.sum(diff) / (size * size * 3)
            if score < 0.05:
                #print(score, ' similar')
                index.append(j)
            j+=1
        print('time',time.time()-start)
        for k in reversed(index):
            imgs.pop(k)
            shutil.move(path + files[k], r'G:/data/ITC/longmao_20190116/kettle/kettle/chongfu/' + files[k])
        files=os.listdir(path)
        i+=1

    print((time.time()-start)/60)

if __name__ == '__main__':
    path = r'G:/data/ITC/longmao_20190116/kettle/kettle/Images'
    size = 300
    main()