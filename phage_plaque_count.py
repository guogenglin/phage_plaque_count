# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 00:25:15 2023

@author: Genglin Guo
"""

from imutils import contours
import imutils
import cv2
import numpy as np
import sys

def cv_show(name,img):
    # Rapid picture visualization
	cv2.imshow(name, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
    
def plate_size_normalization(phage_plate):
    #find the external of plate and normalize the picture
    gray = cv2.cvtColor(phage_plate, cv2.COLOR_BGR2GRAY)
    bi_gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)) # a big kernel will be effective for erase the small noisy point
    bi_gray_cl = cv2.morphologyEx(bi_gray, cv2.MORPH_OPEN, sqKernel) # an opening operation is useful for erase the write small noisy point
    # repeat the closing operation to make the edge of plate smooth (sometimes the reflection will affect the controur finding )
    for i in range(10):
        bi_gray_cl = cv2.morphologyEx(bi_gray_cl, cv2.MORPH_CLOSE, sqKernel) 
        extercnt, hierarchy = cv2.findContours(bi_gray_cl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(extercnt) == 1:
            break
    # Choose the biggest contours——plate, to resize the picture
    if len(extercnt) > 1:
        ax, ay, aw, ah, arclength = 0, 0, 0, 0, 0
        for i in extercnt:
            temlength = cv2.arcLength(i, True)
            if temlength > arclength:
                ax, ay, aw, ah = cv2.boundingRect(i)
                arclength = temlength
    phage_plate_resize = imutils.resize(phage_plate[ay : ay + ah, ax : ax + aw], width = 600)
    return phage_plate_resize

def Positioning_plaques(phage_plate):
    gray = cv2.cvtColor(phage_plate, cv2.COLOR_BGR2GRAY)
    # Filter the noisy point
    Gaussian_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # if the bacteriophage plaque is very clear, auto threshold calculation could be used
    bi_Gaussian_gray = cv2.threshold(Gaussian_gray, 80, 255, cv2.THRESH_BINARY)[1]
    sqKernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # To make the edge of plate smooth
    for i in range (10):
        bi_Gaussian_gray = cv2.morphologyEx(bi_Gaussian_gray, cv2.MORPH_CLOSE, sqKernel1) 
    # find all contours
    allcontours, hierarchy = cv2.findContours(bi_Gaussian_gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all contours and remove the contour of plate
    allcontours_sorted = contours.sort_contours(allcontours, method="left-to-right")[0][1:]
    return allcontours_sorted

def filter_the_plaques(plate, potential_plaque_loc):
    centerX, centerY = plate.shape[1] / 2, plate.shape[0] / 2
    targets = []
    counts = 0
    for i in potential_plaque_loc:
	# Calculate the distance from minEnclosingCircle of contours to the midpoint of plate
        (x, y), radius = cv2.minEnclosingCircle(i)
        distance = ((x - centerX) ** 2 + (y - centerY) ** 2) ** 0.5
    # Calculate the width-height ratio of boundingRect
        _, _, w, h = cv2.boundingRect(i)
        ar = w / float(h)
        # Remove the mismatch caused by impurity in culture agar
        if radius < 2:
            continue
        # filter mismatch in the edge of plate, if the distance is bigger than radius of plate - 10, then continue
        if distance < min(centerX, centerY) - 10:
            targets.append(i)
            counts += 1
            # In case of one match contains many overlapped plaques
            if ar >= 1.5:
                counts += int(ar)
    return targets, counts

def output(plate, plagues, counts):
    marked_picture = cv2.drawContours(plate.copy(), plagues, -1, (0, 0, 255), 3) 
    cv_show('marked_picture', marked_picture)
    print('A total number of {} bacteriophage plaques were detected on the plate'.format(str(counts)))  

def main():
    print('If you have any quesions or suggestions for SsuisChara, please contact Genglin Guo, e-mail: 2019207025@njau.edu.cn')
    file_name = sys.argv[1:]
    for inputfile in file_name:
        phage_plate = cv2.imread(inputfile)
        phage_plate_resize = plate_size_normalization(phage_plate)
        potential_plaque_loc = Positioning_plaques(phage_plate_resize)
        plagues, counts = filter_the_plaques(phage_plate_resize, potential_plaque_loc)
        output(phage_plate_resize, plagues, counts)
        
main()
