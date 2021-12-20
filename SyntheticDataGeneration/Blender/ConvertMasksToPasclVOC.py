# This code converts the masks provided by blender into formatted lables data
# The format used is Pascal VOC
# Check https://github.com/AsherBarak/lego-ai-fun for more details.
#
# All rights reserved

import cv2
#import matplotlib
import numpy as np
#from matplotlib import pyplot as plt
import os
from lxml import etree

##############################
# Utils

def is_file_mask(file):
    # todo: replace with effective logic
    return file.name.startswith('Dec')
    return not(file.name.startswith('Image')) and not(file.name.startswith('demo'))

def is_file_image(file):
    return file.name.startswith('Image')

def generate_folder_PascalVOC(image_folder_path):
    masks=list()
    img=[]
    imageFile=''

    for file in os.scandir(image_folder_path):
        if file.is_file():
            if is_file_image(file):
                imageFile=file
                img =cv2.imread(file.path,cv2.IMREAD_ANYCOLOR)
            if is_file_mask(file):
                masks.append((file,cv2.imread(file.path,cv2.IMREAD_GRAYSCALE)))

    root = etree.Element("annotation")
    print(root)
    filename=etree.SubElement(root, "filename")
    filename.text=imageFile.name
    etree.SubElement(root, "path").text=imageFile.path
    size = etree.SubElement(root, "size")
    etree.SubElement(size, "width").text=str(img.shape[1])
    etree.SubElement(size, "width").text=str(img.shape[0])
    etree.SubElement(size, "depth").text=str(img.shape[2])

    for mask in masks:
        contours,_=cv2.findContours(mask[1],1,1)
        if len(contours)>0:
            x,y,w,h = cv2.boundingRect(contours[0])
            img=cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
            brick_name=mask[0].name.split("_")[5]
            object=etree.SubElement(root,"object")
            etree.SubElement(object, "name").text=brick_name
            bndbox=etree.SubElement(object,"bndbox")
            etree.SubElement(bndbox, "xmin").text=str(x)
            etree.SubElement(bndbox, "ymin").text=str(y)
            etree.SubElement(bndbox, "xmax").text=str(x+w)
            etree.SubElement(bndbox, "xmax").text=str(y+h)

    cv2.imwrite(image_folder_path+"/masks.jpg",img)
    et = etree.ElementTree(root)
    et.write(image_folder_path+'/output.xml', pretty_print=True)

##############################
# Script content

image_folder_path='C:/temp/Dec_19_17_51_1'
for el in os.scandir('c:/temp'):
    try:
        if (el.is_dir()):
            generate_folder_PascalVOC(el.path)
    except:
        print(el.path)

