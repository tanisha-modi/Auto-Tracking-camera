# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 15:39:33 2022

@author: rnmic
"""

import cv2
import cv2.aruco as aruco
import numpy as np
import math
from time import sleep

print("Starting")

def findArucoMarkers(img, markerSize=4, totalMarkers=250, draw=True):
    arucoDict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(img, arucoDict, parameters=arucoParam)
    
    if draw:
        aruco.drawDetectedMarkers(img,bbox)
    return bbox, ids, rejected

def getDesired(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Get aruco
    bbox, ids, rejected = findArucoMarkers(img, markerSize=4, totalMarkers=250, draw=True)
    
    if np.any(ids == None):
        ret = 0
        centre = None
    else:
        bboxtl = bbox[0][0][0][0],bbox[0][0][0][1]
        bboxbr = bbox[0][0][2][0],bbox[0][0][2][1]

        centre = getCentre(bboxtl,bboxbr)
        ret = 1
        print(centre)
    return centre, ret

class arucoMarker():
    def __init__(self):
        self.bboxtl = None
        self.bboxbr = None
        self.centre = None
    
    def getCentre(bboxtl,bboxbr):
        centre = int((bboxtl[0]+bboxbr[0])/2), int((bboxtl[1]+bboxbr[1])/2)
        return centre
    
def getArucos(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Get aruco
    arucos = list()
    bboxs, ids, rejected = findArucoMarkers(img, markerSize=4, totalMarkers=250, draw=True)
    
    if np.any(ids == None):
        ret = 0
    else:
        for bbox in bboxs:
            aruco = arucoMarker()
            aruco.bboxtl = bbox[0][0][0],bbox[0][0][1]
            aruco.bboxbr = bbox[0][2][0],bbox[0][2][1]
            aruco.centre = arucoMarker.getCentre(aruco.bboxtl,aruco.bboxbr)
            
            arucos.append(aruco)
        
        ret = 1
    return arucos, ret

def getAdjustment(windowMax, x):
    normalised_adjustment = x/windowMax - 0.5
    adjustment_magnitude = abs(round(normalised_adjustment,1))

    if normalised_adjustment>0:
        adjustment_direction = -1
    else:
        adjustment_direction = 1
        
    return adjustment_magnitude, adjustment_direction

def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

vid = cv2.VideoCapture(0)
print("Video started")

while(True):
    # Get image
    ret, img = vid.read()
    img = rescale_frame(img,50)
    window = img.shape
    
    # Get arucos
    arucos, ret = getArucos(img)
    
    if ret == 0:
        pass
    else:
            
        # Calculate AB (pixel error)
        A = (0,0)
        B = arucos[0].centre
        
        # show image
        cv2.imshow("image",img)
        cv2.waitKey(1)
        
        # Get adjustment
        xmag, xdir = getAdjustment(window[0],B[1])
        ymag, ydir = getAdjustment(window[1],B[0])

        if xmag != None:
            
            # Print servo angles
            servo1_angle = cx * xdir * xmag
            servo2_angle = cy * ydir * ymag
            print("Servo 1 Angle:", servo1_angle)
            print("Servo 2 Angle:", servo2_angle)
         
        xmag = 0
        xdir = 0
        ymag = 0
        ydir = 0
