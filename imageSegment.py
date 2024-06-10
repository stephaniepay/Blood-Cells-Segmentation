# -*- coding: utf-8 -*-
"""
imageSegment.py

YOUR WORKING FUNCTION

"""
import cv2
import numpy as np

input_dir = 'dataset/input'
output_dir = 'dataset/output'

# you are allowed to import other Python packages above
##########################
def segmentImage(inputImg):
    # Inputs
    # img: Input image, a 3D numpy array of row*col*3 in BGR format
    #
    # Output
    # outImg: segmentation image
    #
    #########################################################################
    # ADD YOUR CODE BELOW THIS LINE
    
    #image sharpening
    median = cv2.medianBlur(inputImg, 5) 
    smoothened = cv2.blur(median, (5,5))
    details = median - smoothened
    img = median + details
    
    #image format conversion
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #set kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    
    #White Blood
    white_lower = np.array([110, 40, 180])
    white_upper = np.array([155, 145, 240])
    mask_whiteblood = cv2.inRange(img, white_lower, white_upper)
    mask_whiteblood = cv2.morphologyEx(mask_whiteblood, cv2.MORPH_CLOSE, kernel, iterations=9)
    mask_whiteblood = cv2.morphologyEx(mask_whiteblood, cv2.MORPH_OPEN, kernel, iterations=9)
    mask_whiteblood = cv2.medianBlur(mask_whiteblood, 15)

    #Red Blood  
    redblood_lower = np.array([150, 0, 140]) 
    redblood_upper = np.array([210, 80, 220])
    mask_redblood = cv2.inRange(img, redblood_lower, redblood_upper)
    mask_redblood = cv2.dilate(mask_redblood, kernel, iterations=6)
    mask_redblood = cv2.morphologyEx(mask_redblood, cv2.MORPH_OPEN, kernel, iterations=1)
    mask_redblood = cv2.medianBlur(mask_redblood, 15)
        
    #Background
    bg_lower = np.array([20, 0, 180]) 
    bg_upper = np.array([140, 35, 220])
    mask_bg = cv2.inRange(img, bg_lower, bg_upper)
    mask_bg = cv2.morphologyEx(mask_bg, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask_bg = cv2.morphologyEx(mask_bg, cv2.MORPH_OPEN, kernel, iterations=3)
    mask_bg = cv2.medianBlur(mask_bg, 15)
   
    outputImg = mask_whiteblood + mask_redblood + mask_bg
    outputImg[:,:][np.where(mask_redblood)] = [2]
    outputImg[:,:][np.where(mask_whiteblood)] = [1]
    outputImg[:,:][np.where(mask_bg)] = [0]
 
    # END OF YOUR CODE
    #########################################################################
    return outputImg
