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
import sys

##############################
# Utils

def is_file_mask(file):
    #return file.name.startswith('Dec') and file.name.endswith('.png')
    return file.name.startswith('Mask_')

def is_file_image(file):
    #return file.name.startswith('Dec') and file.name.endswith('.jpg')
    return file.name.startswith('Img_') and file.name.endswith('.jpg')

def get_mask_bounding_box(mask_image):
        
    xmin=0
    xmax=0
    ymin=0
    ymax=0

    for x in range(mask_image.width):
        for y in range(mask_image.height):
            p=mask_image.getpixel((x,y))
            if p:
                if xmin==0: xmin=x 
                else: xmax=x
                if ymin==0: ymin=y 
                else: ymax=y
    return xmin, ymin, xmax, ymax


################################

def generate_folder_PascalVOC(image_folder_path):
    masks=list()
    img=[]
    imageFile=''

    folder_name=os.path.basename(os.path.normpath(image_folder_path))
    # os.rename(image_folder_path+'\\Image.jpg', image_folder_path+'\\'+folder_name+'.jpg')

    for file in os.scandir(image_folder_path):
        if file.is_file():
            if is_file_image(file):
                imageFile=file
                img =cv2.imread(file.path,cv2.IMREAD_ANYCOLOR)
            if is_file_mask(file):
                masks.append((file,cv2.imread(file.path,cv2.IMREAD_GRAYSCALE)))

    root = etree.Element("annotation")
    print(root)
    etree.SubElement(root, "folder")
    filename=etree.SubElement(root, "filename")
    filename.text=imageFile.name
    source=etree.SubElement(root, "source")
    etree.SubElement(source, "database").text="legoaifun"
    etree.SubElement(root, "source")
    etree.SubElement(root, "path").text=imageFile.path
    etree.SubElement(root, "segmented").text="0"
    size = etree.SubElement(root, "size")
    etree.SubElement(size, "width").text=str(img.shape[1])
    etree.SubElement(size, "height").text=str(img.shape[0])
    etree.SubElement(size, "depth").text=str(img.shape[2])

    for mask in masks:
        contours,_=cv2.findContours(mask[1],1,1)
        if len(contours)>0:

            boxes=[]
            for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)
                boxes.append([x,y, x+w,y+h])

            boxes = np.asarray(boxes)
            left, top = np.min(boxes, axis=0)[:2]
            right, bottom = np.max(boxes, axis=0)[2:]

            # x,y,w,h = cv2.boundingRect(contours[0])
            img=cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),1)
            brick_name=mask[0].name.split("_")[6]
            object=etree.SubElement(root,"object")
            etree.SubElement(object, "name").text=brick_name
            etree.SubElement(object, "pose").text="Unspecified"
            etree.SubElement(object, "truncated").text="0"
            etree.SubElement(object, "difficult").text="0"
            etree.SubElement(object, "occluded").text="0"
            bndbox=etree.SubElement(object,"bndbox")
            etree.SubElement(bndbox, "xmin").text=str(left)
            etree.SubElement(bndbox, "ymin").text=str(top)
            etree.SubElement(bndbox, "xmax").text=str(right)
            etree.SubElement(bndbox, "ymax").text=str(bottom)

    cv2.imwrite(image_folder_path+"/masks.jpg",img)
    et = etree.ElementTree(root)

    
    #et.write(image_folder_path+'/'+folder_name+'.xml', pretty_print=True)
    et.write(imageFile.path.replace('jpg','xml'), pretty_print=True)

##############################
# Script content

for el in os.scandir('C:\\temp\\Dec_21_23_01'):
    if (el.is_dir()):
                generate_folder_PascalVOC(el.path)
    try:
        if (el.is_dir()):
            generate_folder_PascalVOC(el.path)
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        print(el.path)

