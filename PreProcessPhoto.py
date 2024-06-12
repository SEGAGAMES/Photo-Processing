#!/usr/bin/python
# -*- coding: cp1251  -*-
import cv2
from cv2.typing import MatLike
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from ImageUpdate import ImageUpdate

class Otladka(): # Класс для отладки фото.
    def ShowImages(images:[], axes:bool=False): # Выводит все изображения массива в одном окне.
        if (len(images) > 1):
            f, axarr = plt.subplots(1,len(images)) 
            for i in range(len(images)):
                axarr[i].imshow(images[i])
        else:
            plt.imshow(images[0])
        plt.show()
    
class PreProcessPhoto():
    
    def _Find_biggest_countour(contours:[MatLike]): # Поиск наибольшего контура.
        maxx = contours[0]
        for item in contours:
            if (cv2.contourArea(item) > cv2.contourArea(maxx)):
                maxx = item
        return maxx
    
    def FindWithPath(path: str, all: bool) -> []: # Перебор вариантов контура. 
        bestimage = []
        image = cv2.imread(path)
        ans = PreProcessPhoto._TryContour(image,150)  
        if (len(ans) != 1):
            max_image = ans
            bestimage.append(ans)
        else:
            max_image = [0]
        i = 150
        while i - 5 > 150-50:
            i = i-5
            ans = PreProcessPhoto._TryContour(image,i)
            if (len(ans) == 1):
                continue
            if (len(max_image) == 1):
                max_image = ans
            if (ans.shape[0] +ans.shape[1]  > max_image.shape[0]+max_image.shape[1]):
                max_image = ans
                bestimage.append(ans)
                
        i = 150
        while i + 5 < 150+50:
            i = i +5
            ans = PreProcessPhoto._TryContour(image,i)
            if (len(ans) == 1):
                continue
            if (len(max_image) == 1):
                max_image = ans
            if (ans.shape[0] +ans.shape[1]  > max_image.shape[0]+max_image.shape[1]):
                max_image = ans
                bestimage.append(ans)
                
        if (all):
            return bestimage
        else:
            return max_image
        
    def Find(image:MatLike, all: bool) -> []: # Перебор вариантов контура. 
        bestimage = []
        ans = PreProcessPhoto._TryContour(image,150)   
        if (len(ans) != 1):
            max_image = ans
            bestimage.append(ans)
        else:
            max_image = [0]
        
        i = 150
        while i - 5 > 150-50:
            i = i-5
            ans = PreProcessPhoto._TryContour(image,i)
            if (len(ans) == 1):
                continue
            if (len(max_image) == 1):
                max_image = ans
            if (ans.shape[0] +ans.shape[1]  > max_image.shape[0]+max_image.shape[1]):
                max_image = ans
                bestimage.append(ans)
                
        i = 150
        while i + 5 < 150+50:
            i = i +5
            ans = PreProcessPhoto._TryContour(image,i)
            if (len(ans) == 1):
                continue
            if (ans.shape[0] +ans.shape[1]  > max_image.shape[0]+max_image.shape[1]):
                max_image = ans
                bestimage.append(ans)
                
        if (all):
            return bestimage
        else:
            return max_image
                
    def _TryContour(image:MatLike, thresh:int=150) -> []: # Подбор контура с заданным параметром цветокоррекции.
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont = PreProcessPhoto._Find_biggest_countour(contours)        
        approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
        
        if (len(approx) == 4):
            return PreProcessPhoto._GetPerspectiveTransform(approx, image)
        else:
            return [0]
        
    def _GetPerspectiveTransform(approx, image): # Обрезка изображения по контуру.
        (pt_A, pt_B, pt_C, pt_D) = PreProcessPhoto._FindPointsToRotate(approx)
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

    def _FindPointsToRotate(approx):
        pt_A = approx[0][0]
        pt_B = approx[1][0]
        pt_C = approx[2][0]
        pt_D = approx[3][0]
        step = 0 
        while (pt_A[1]>pt_B[1] or pt_B[0]>pt_C[0] or pt_C[1]<pt_D[1] or pt_A[0]>pt_D[0]):
            (pt_A, pt_B, pt_C, pt_D) = (pt_D, pt_A, pt_B, pt_C)
            step = step + 1
            if step > 4:
                break
        return (pt_A, pt_B, pt_C, pt_D)
    
    def GetBestPhotosWithImage(image:MatLike):
        return PreProcessPhoto.Find(image, True)
    def GetBestPhotos(path:str):
        return PreProcessPhoto.FindWithPath(path, True)
    def GetPreprocessPhoto():
        root = tk.Tk()
        root.withdraw()  # скрываем главное окно
        file_path = filedialog.askopenfilename()  # вызываем диалоговое окно
        image = PreProcessPhoto.Find(file_path, False)
        result = ImageUpdate.Update(image)
        Otladka.ShowImages([cv2.imread(file_path),image, result])






