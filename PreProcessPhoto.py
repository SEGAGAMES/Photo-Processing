#!/usr/bin/python
# -*- coding: cp1251  -*-
from hmac import new
import cv2
import numpy as np
import matplotlib.pyplot as plt

from ImageUpdate import ImageUpdate

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
        
        binary1 = PreProcessPhotov2.RGB(image)
        # approx = PreProcessPhotov2.FindApprox(binary1)
        # value  = PreProcessPhotov2.ApproxImage(image, approx)
        
        binary2 = PreProcessPhotov2.HLS(image) # HLS - по "светлоте фото"
        # approx = PreProcessPhotov2.FindApprox(binary2)
        # HLS = PreProcessPhotov2.ApproxImage(image, approx)
        
        binary3 = PreProcessPhotov2.HSV(image) # HSV - по "значению цвета"
        # approx = PreProcessPhotov2.FindApprox(binary3)
        # HSV = PreProcessPhotov2.ApproxImage(image, approx)
        
        binary4 = PreProcessPhotov2.gray(image) # Без обработки
        # approx = PreProcessPhotov2.FindApprox(binary4)
        # gray = PreProcessPhotov2.ApproxImage(image, approx)
        binaryall = np.copy(binary1)
        for item in range(len(binary1)):
            for pixel in range(len(binary1[item])):
                binaryall[item][pixel]=0
                summ = int(int(binary2[item][pixel][1])+int(binary3[item][pixel][2])+int(binary4[item][pixel]))
                if summ >= 400:
                    binaryall[item][pixel]=255
                else:
                    binaryall[item][pixel]=0
        Otladka.ShowImages([binary1,binary2,binary3,binary4, binaryall])
        approx = PreProcessPhotov2.FindApprox(binaryall)
        gray = PreProcessPhotov2.ApproxImage(image, approx)
        if gray is None:
            for item in range(len(binary1)):
                for pixel in range(len(binary1[item])):
                    binaryall[item][pixel]=0
                    summ = int(int(binary2[item][pixel])+int(binary3[item][pixel])+int(binary4[item][pixel]))
                    if summ >= 255:
                        binaryall[item][pixel]=255
                    else:
                        binaryall[item][pixel]=0
        approx = PreProcessPhotov2.FindApprox(binaryall)
        gray = PreProcessPhotov2.ApproxImage(image, approx)
        return [binary1, binary2, binary3,  binary4, binaryall, gray]
        # return [value, HLS, HSV , gray]
    def RGB(image):
        copy = np.copy(image)
        copy = cv2.normalize(copy,  None, 200, 0, cv2.NORM_INF)
        cp = np.copy(copy)
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
        # Otladka.ShowImages([cp,copy, newgray,binary])
        return binary
    def HLS(image):
        copy = np.copy(image)
        # gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
        newgray = cv2.normalize(copy,  None, 150, 255, cv2.NORM_INF)
        # Otladka.ShowImages([newgray])
        # normalized_color_image = cv2.cvtColor(newgray, cv2.COLOR_GRAY2BGR)
        # for y in range(newgray.shape[0]):
        #     for x in range(newgray.shape[1]):
        #         for c in range(newgray.shape[2]):
        #             newgray[y,x,c] = np.clip(2*newgray[y,x,c] + 0, 0, 255)
        HLS = cv2.cvtColor(newgray, cv2.COLOR_RGB2HLS)
        HLS2 = cv2.cvtColor(copy, cv2.COLOR_RGB2HLS)
        # Otladka.ShowImages([newgray,HLS, HLS2])
        for item in HLS:
            for pixel in item:
                if pixel[1]  >= pixel[0]*1.5:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255                  
                else:
                    pixel[0] = 0
                    pixel[2] = 0
                    pixel[1] = 0
        newgray = cv2.cvtColor(HLS, cv2.COLOR_BGR2GRAY)
        # Otladka.ShowImages([HLS, HLS2,newgray])
        return HLS2
    def HSV(image):
        copy = np.copy(image)
        newgray = cv2.normalize(copy,  None, 100, 200, cv2.NORM_INF )

        HSV = cv2.cvtColor(copy, cv2.COLOR_RGB2HSV_FULL)
        # Otladka.ShowImages([newgray, HSV])
        sredVal= 0
        sredSat= 0
        count = 0
        for item in HSV:
            for pixel in item:
                sredVal= sredVal + int(pixel[2])
                sredSat = sredSat + int(pixel[1])
                count = count +1
        sredVal = sredVal / count
        sredSat = sredSat / count
        # print(sredVal)
        # print(sredSat)
        # if sredSat > 50:
        #     print(sredSat)
        #     return None
        cp = np.copy(HSV)
        for item in HSV:
            for pixel in item:   
                if pixel[1] < sredSat and pixel[2] > sredVal*1.2:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255                  
                else:
                    pixel[0] = 0
                    pixel[1] = 0
                    pixel[2] = 0
        # Otladka.ShowImages([HSV])
        newgray = cv2.cvtColor(HSV, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, 200, 255, cv2.THRESH_BINARY)
        # Otladka.ShowImages([cp,HSV,binary])
        return cp
    def gray(image):
        copy = np.copy(image)
        newgray = cv2.normalize(copy,  None, 150, 255, cv2.NORM_INF)
        sred = 0
        count = 0
        for item in newgray:
            for pixel in item:
                sred = int(sred+int(pixel[0]))
                count = count +1
        sred = sred / count
        # print(sred)
        newgray = cv2.cvtColor(newgray, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, sred*1.5, 255, cv2.THRESH_BINARY)
        # Otladka.ShowImages([newgray,binary])
        return binary
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
            print("approx problem")
            return None
        return PreProcessPhotov2._GetPerspectiveTransform(approx, image)
PreProcessPhotov2.Work("D:\\repos\\Photo-Processing\\example.jpg")
PreProcessPhotov2.Work("D:\\repos\\Photo-Processing\\example2.jpg")
# PreProcessPhotov2.Work()
        







