import os
import sys


###class_list = ["apple","banana"]


#class_list = ["apple"]



train_list = []
test_list = []
val_list = []


train_file = open("train.txt",'w')
test_file = open("test.txt",'w')
val_file = open("val.txt",'w')

#len_list = []
################folder=["suitcase"]

#########################folder=["pineapple"]#, "lawn", "plant", "plant_duorou"]

folder=["macaron","mango","peach","pear","pudding"]

for m in range(0,len(folder)):

	filelist = os.listdir("./image/"+folder[m]+"/")


	len_c = len(filelist)

	for num in range(len_c):
#'''1/3  train.txt 1/3 test.txt 1/3 val.txt'''
		if num <= int(8*len_c/10):
			train_list.append(filelist[num])
		elif num > int(8*len_c/10) and num <= int(9*len_c/10):
			test_list.append(filelist[num])
		else:
			val_list.append(filelist[num])



for num in range(len(train_list)):
	train_file.write(train_list[num]+"\n")
train_file.close()


for num in range(len(test_list)):
	test_file.write(test_list[num]+"\n")
test_file.close()


for num in range(len(val_list)):
	val_file.write(val_list[num]+"\n")
val_file.close()
#print(filelist)

##def gen(inpath,outpath):
##	file_in 