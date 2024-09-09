#!/usr/bin/python
# -*- coding: cp1251  -*-
from hmac import new
import cv2
import numpy as np
import matplotlib.pyplot as plt

from ImageUpdate import ImageUpdate
from TextReader import TextReader

class Otladka(): # Класс для отладки фото.
    def ShowImages(images:np.ndarray): # Выводит все изображения массива в одном окне.
        if (len(images) > 1):
            _, axarr = plt.subplots(1,len(images)) 
            for i in range(len(images)):
                axarr[i].imshow(images[i])
        else:
            plt.imshow(images[0])
        plt.show()
    

class PreProcessPhotov2():
    def OpenImage(pathorimage):
        if (type(pathorimage) == str):
            image = cv2.imread(pathorimage)
        elif (type(pathorimage) == np.ndarray):
            image = pathorimage
        else:
            raise Exception("Неправильный тип данных")
        return image
    
    def Work(pathorimage):
        image = PreProcessPhotov2.OpenImage(pathorimage) # Открытие изображения.
        
        kernelforopenig = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))  
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernelforopenig)
        
        kernelforclosing = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))  
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelforclosing)

        binary2 = PreProcessPhotov2.HLS(closing) # HLS - по "светлоте фото"
        
        binary3 = PreProcessPhotov2.HSV(closing) # HSV - по "значению цвета"
        
        binary4 = PreProcessPhotov2.gray(closing) # Без обработки
        
        value = 350
        gray = None
        while gray is None:
            gray = PreProcessPhotov2.try_value(image,binary2,binary3,binary4, value)
            value = value - 25
        result = PreProcessPhotov2.hide_shadows(gray)

        return [gray,result]
    def RGB(image):
        copy = np.copy(image)
        copy = cv2.normalize(copy,  None, 200, 0, cv2.NORM_INF)
        for item in copy:
            for pixel in item:
                if pixel[0] > 100 and pixel[1] > 100 and pixel[2] > 100:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255                  
                else:
                    pixel[0] = 0
                    pixel[2] = 0
                    pixel[1] = 0
        newgray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, 200, 255, cv2.THRESH_BINARY)
        return binary
    def HLS(image):
        copy = np.copy(image)
        # newgray = cv2.normalize(copy,  None, 150, 255, cv2.NORM_INF)
        # HLS = cv2.cvtColor(newgray, cv2.COLOR_RGB2HLS)
        HLS2 = cv2.cvtColor(copy, cv2.COLOR_RGB2HLS)
        # for item in HLS:
        #     for pixel in item:
        #         if pixel[1]  >= pixel[0]*1.5:
        #             pixel[0] = 255
        #             pixel[1] = 255
        #             pixel[2] = 255                  
        #         else:
        #             pixel[0] = 0
        #             pixel[2] = 0
        #             pixel[1] = 0
        # newgray = cv2.cvtColor(HLS, cv2.COLOR_BGR2GRAY)
        return HLS2
    def HSV(image):
        copy = np.copy(image)
        # newgray = cv2.normalize(copy,  None, 150, 255, cv2.NORM_INF )

        HSV = cv2.cvtColor(copy, cv2.COLOR_RGB2HSV_FULL)
        # sredVal= 0
        # sredSat= 0
        # count = 0
        # for item in HSV:
        #     for pixel in item:
        #         sredVal= sredVal + int(pixel[2])
        #         sredSat = sredSat + int(pixel[1])
        #         count = count +1
        # sredVal = sredVal / count
        # sredSat = sredSat / count
        # print(sredVal)
        # print(sredSat)
        # if sredSat > 50:
        #     print(sredSat)
        #     return None
        # cp = np.copy(HSV)
        # for item in HSV:
        #     for pixel in item:   
        #         if pixel[1] < sredSat and pixel[2] > sredVal*1.2:
        #             pixel[0] = 255
        #             pixel[1] = 255
        #             pixel[2] = 255                  
        #         else:
        #             pixel[0] = 0
        #             pixel[1] = 0
        #             pixel[2] = 0
        # # Otladka.ShowImages([HSV])
        # newgray = cv2.cvtColor(HSV, cv2.COLOR_BGR2GRAY)
        # _, binary = cv2.threshold(newgray, 200, 255, cv2.THRESH_BINARY)
        # Otladka.ShowImages([cp,HSV,binary])
        return HSV
    def gray(image):
        copy = np.copy(image)
        newgray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, 0, 255, cv2.THRESH_BINARY)
        return binary
    def hide_shadows(image):
        if image is None:
            return None
        rgb_planes = cv2.split(image)

        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_norm_planes.append(norm_img)
            # Otladka.ShowImages([dilated_img,bg_img,diff_img,norm_img])
        result_norm = cv2.merge(result_norm_planes)
        return result_norm
    def try_value(image, binary2, binary3, binary4, value):
        result = np.copy(binary4)
        for item in range(len(binary2)):
            for pixel in range(len(binary2[item])):
                result[item][pixel]=0
                summ = int(int(binary2[item][pixel][1])+int(binary3[item][pixel][2]))
                if summ >= value:
                    result[item][pixel]=255
                else:
                    result[item][pixel]=0
        approx = PreProcessPhotov2.FindApprox(result)
        gray = PreProcessPhotov2.ApproxImage(image, approx)
        return gray
    
    def FindApprox(binary):
        if binary is None:
            return [0]
        kernelforclosing = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))  
        closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernelforclosing)

        kernelforopenig = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))  
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernelforopenig)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))  
        dilated = cv2.dilate(opening, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if (contours is None or len(contours) == 0):
            return [0]
        contour = max(contours, key = cv2.contourArea)

        approx = cv2.approxPolyDP(contour, 0.049 * cv2.arcLength(contour, True), True)
        
        return approx
    
    def _GetPerspectiveTransform(approx:np.ndarray, image:np.ndarray) -> np.ndarray: # Обрезка изображения по контуру.
        # Поворот точек контура.
        if PreProcessPhotov2._FindPointsToRotate(approx) is None:
            return None
        (pt_A, pt_B, pt_C, pt_D) = PreProcessPhotov2._FindPointsToRotate(approx)
        # Обрезка изображения. НЕ ТРОГАТЬ
        width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
        width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
        maxWidth = max(int(width_AD), int(width_BC))
        height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
        height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
        maxHeight = max(int(height_AB), int(height_CD))
        input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
        output_pts = np.float32([[ 0,0],
                                [0, maxHeight - 1],
                                [maxWidth - 1, maxHeight - 1],
                                [maxWidth - 1, 0]])
        M =  cv2.getPerspectiveTransform(input_pts,output_pts)
        return cv2.warpPerspective(image,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)

    def _FindPointsToRotate(approx: np.ndarray):
        pt_A = approx[0][0]
        pt_B = approx[1][0]
        pt_C = approx[2][0]
        pt_D = approx[3][0]
        step = 0 
        while (pt_A[1]>pt_B[1] or pt_B[0]>pt_C[0] or pt_C[1]<pt_D[1] or pt_A[0]>pt_D[0]):
            (pt_A, pt_B, pt_C, pt_D) = (pt_D, pt_A, pt_B, pt_C)
            step = step + 1
            if step > 10:
                return None
        return (pt_A, pt_B, pt_C, pt_D)
    
    def ApproxImage(image, approx):    
        if len(approx) != 4:
            return None
        return PreProcessPhotov2._GetPerspectiveTransform(approx, image)

        







