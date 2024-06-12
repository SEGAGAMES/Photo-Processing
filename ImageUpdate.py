#!/usr/bin/python
# -*- coding: cp1251  -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageUpdate():
    def Update(path:str):
        img = cv2.imread(path)
        dilated_img = cv2.dilate(img, np.ones((7,7), np.uint8)) 
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(img, bg_img)
        norm_img = diff_img.copy() # Needed for 3.x compatibility
        cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
        result = cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        _, binary = cv2.threshold(result, 200, 255, cv2.THRESH_BINARY)
        # Otladka([img, dilated_img,bg_img, diff_img, norm_img, result])
        # Otladka([img,result, binary])
    def Update(image:[]):
        dilated_img = cv2.dilate(image, np.ones((7,7), np.uint8)) 
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(image, bg_img)
        norm_img = diff_img.copy() # Needed for 3.x compatibility
        cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
        result = cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        _, binary = cv2.threshold(result, 225, 255, cv2.THRESH_BINARY)
        return binary
        # Otladka([img, dilated_img,bg_img, diff_img, norm_img, result])
        # Otladka([image, binary])
# ImageUpdate.Update("D:\\1.jpg")

