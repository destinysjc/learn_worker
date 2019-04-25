from PIL import Image
import os
import shutil

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
    print(jpg_file_path)
    # print("-------------")
            
    return jpg_file_name, jpg_file_path



def is_jpg(filename, move_dir):  
 
    data = Image.open(filename)
    if data.format =='JPEG':
        print(filename, "是JPEG文件")
    else:
         isExists=os.path.exists(move_dir)
         if not isExists:
             os.makedirs(move_dir)
             shutil.move(filename, move_dir)
             print(filename, '--move---->>>', move_dir)
        
def is_or_jpg(filename, move_dir):
    data = open(filename,'rb').read(11)
    if data[:4] != '\xff\xd8\xff\xe0' and data[:4]!='\xff\xd8\xff\xe1': 
        isExists=os.path.exists(move_dir)
        if not isExists:
            os.makedirs(move_dir)
            shutil.move(filename, move_dir)
            print(filename, '--move---->>>', move_dir)
    elif data[6:] != 'JFIF\0' and data[6:] != 'Exif\0': 
        isExists=os.path.exists(move_dir)
        if not isExists:
            os.makedirs(move_dir)
            shutil.move(filename, move_dir)
            print(filename, '--move---->>>', move_dir)
    else:
        print(filename, "是JPEG文件")


if __name__ == "__main__":
    jpg_path = r'../workTrains/train_ssdlite/image/test'
    move_path = r'../workTrains/train_ssdlite/image/move_dir/test'
    jpg_file_name, jpg_file_path = get_file_name_path(jpg_path, '.jpg')
    for fp in jpg_file_path:
        is_jpg(fp, move_path)
        is_or_jpg(fp, move_path)
     