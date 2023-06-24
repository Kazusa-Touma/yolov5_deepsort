import cv2
import numpy as np
import glob
import os

# 其它格式的图片也可以
img_array = []
for filename in glob.glob('D:/yolo5/dataset/DETRAC-train-data/Insight-MVT_Annotation_Train/MVI_40963/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

# avi：视频类型，mp4也可以
# cv2.VideoWriter_fourcc(*'DIVX')：编码格式
# 5：视频帧率
# size:视频中图片大小
out = cv2.VideoWriter('D:/download/bilibili-yolov5_deepsort-main/bilibili-yolov5_deepsort-main/yolov5-deepsort/video/MVI_40963.mp4',
                      cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
