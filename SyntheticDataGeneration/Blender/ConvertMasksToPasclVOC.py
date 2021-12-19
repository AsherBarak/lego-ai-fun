# This code converts the masks provided by blender into formatted lables data
# The format used is Pascal VOC

import cv2
#import matplotlib
import numpy as np
#from matplotlib import pyplot as plt
import os


image_folder_path='C:\temp\Dec_19_17_51_1'


#mask_path='C:/temp/Dec_17_01_01_1/Dec_17_01_01_1_3710_100070.png'
#img_path='C:/temp/Dec_17_01_01_1/image0070.png'
mask_path='C:/temp/Dec_19_17_51_1/Dec_19_17_51_1_98138_110070.png'
img_path='C:/temp/Dec_19_17_51_1/image0070.png'



mask = cv2.imread(mask_path,cv2.IMREAD_GRAYSCALE)
img =cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
contours,_=cv2.findContours(mask,1,1)
x,y,w,h = cv2.boundingRect(contours[0])
with_rect=cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
cv2.namedWindow( "X", cv2.WINDOW_AUTOSIZE )
cv2.imshow('X',with_rect)
cv2.waitKey(0)

