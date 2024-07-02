
import os
import cv2
import matplotlib.pyplot as plt

image_list=[]
file_name_list=[]
def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        file_name_list.append(filename)
        #print(full_filename)
        image_list.append(full_filename)
search("./data_annotated/SegmentationClassPNG")

for i in range(0,len(image_list)):
    iamge = cv2.imread(image_list[i])
    image_gray = cv2.cvtColor(iamge, cv2.COLOR_BGR2GRAY)
    image_gray = image_gray/255
    cv2.imwrite("./data_annotated/SegmentationClassPNG3/"+file_name_list[i],image_gray)