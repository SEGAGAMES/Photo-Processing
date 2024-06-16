#!/usr/bin/python
# -*- coding: cp1251  -*-
from ctypes import OleDLL
import math
import cv2
from cv2.typing import MatLike, Point
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
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
    
class PreProcessPhoto():
    
    def _findBiggestCountour(contours:tuple) -> np.ndarray: # Поиск наибольшего контура.
        maxx = contours[0]
        maxi = 0
        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) > cv2.contourArea(maxx):
                maxx = contours[i]
                maxi = i
        return (maxx, maxi)
    
    def PreProcess(pathorimage, all: bool = True) -> np.ndarray: # Перебор вариантов контура. 
        # Блок проверки входных данных
        if (type(pathorimage) == str):
            image = cv2.imread(pathorimage)
        elif (type(pathorimage) == np.ndarray):
            image = pathorimage
        else:
            raise Exception("Неправильный тип данных")
        if (type(all) != bool):
            raise Exception("Неправильный тип данных")
        
        # Сохранение подходящих изображений.
        bestimage = []
        
        ans = PreProcessPhoto._TryContour(image,150)  
        
        # Проверка что изобрважение обрезалось.
        if ans is not None:
            max_image = ans
            bestimage.append(ans)
        else:
            max_image = None
        # Подбор разных параметров для лучшей обрезки.
        i = 150
        while i - 5 > 50:
            i = i-5
            ans = PreProcessPhoto._TryContour(image,i)
            if ans is None:
                continue
            if max_image is None:
                max_image = ans
                bestimage.append(ans)
            if (ans.shape[0] +ans.shape[1]  > max_image.shape[0]+max_image.shape[1]):
                max_image = ans
                bestimage.append(ans)
                
        i = 150
        while i + 5 < 250:
            i = i +5
            ans = PreProcessPhoto._TryContour(image,i)
            if ans is None:
                continue
            if max_image is None:
                max_image = ans
                bestimage.append(ans)
            if (ans.shape[0] +ans.shape[1]  > max_image.shape[0]+max_image.shape[1]):
                max_image = ans
                bestimage.append(ans)
        # Возврат либо самого большого изображения, либо всех.  
        if (all):
            return bestimage
        else:
            return max_image
           
    def _TryContour(image:np.ndarray, thresh:int=150) -> np.ndarray: # Подбор контура с заданным параметром цветокоррекции.
        # Начальная обработка изображения
        oldgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        old2 = np.copy(gray)
        for item in gray:
            for pixel in item:
                if pixel[0] > pixel[1] and pixel[2] > 200:
                    pixel[0] = 255
                    pixel[1] = 255
                else:
                    pixel[0] = 0
                    pixel[1] = 0
        newgray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        # thresh = 200
        _, binary = cv2.threshold(newgray, thresh, 255, cv2.THRESH_BINARY)
        Otladka.ShowImages([image,oldgray,old2,gray,newgray, binary])
        
        # Поиск границ для нового фото.
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont,ind = PreProcessPhoto._findBiggestCountour(contours)   
        Otladka.ShowImages([cv2.drawContours(image, contours,ind , (255,0,0), 10)])
        # Превращение границ в прямоугольник.
        approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
        
        # Проверка, удалось ли найти 4х-угольник
        if (len(approx) == 4):
            ret = PreProcessPhoto._GetPerspectiveTransform(approx, image)
            Otladka.ShowImages([ret])
            return ret
        else:
            return None
        
    def FindRectangle(pathorimage) -> np.ndarray: # Работающий метод
        
        # Блок проверки входных данных
        if (type(pathorimage) == str):
            image = cv2.imread(pathorimage)
        elif (type(pathorimage) == np.ndarray):
            image = pathorimage
            if image is None:
                raise Exception("Неправильный тип данных")
        else:
            raise Exception("Неправильный тип данных")
        
        # Начальная обработка изображения
        HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        oldHSV = np.copy(HSV)
        for item in HSV:
            for pixel in item:
                if pixel[1] < pixel[0] and pixel[2] > 150:
                    pixel[0] = 255
                    pixel[1] = 255
                else:
                    pixel[0] = 0
                    pixel[1] = 0
        newgray = cv2.cvtColor(HSV, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, 200, 255, cv2.THRESH_BINARY)
        
        # Поиск границ для нового фото.
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont,_ = PreProcessPhoto._findBiggestCountour(contours)   
        
        # Превращение границ в прямоугольник.
        approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
        rect = cv2.boundingRect(approx)
        pt_A = [rect[0], rect[1]]
        pt_B = [rect[0], rect[1]+rect[3]]
        pt_C = [rect[0]+rect[2], rect[1]+rect[3]]
        pt_D = [rect[0]+rect[2], rect[1]]

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
        ret =  cv2.warpPerspective(image,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
        return ret

    def _findContour(pathorimage):
        if (type(pathorimage) == str):
            image = cv2.imread(pathorimage)
        elif (type(pathorimage) == np.ndarray):
            image = pathorimage
        else:
            raise Exception("Неправильный тип данных")
        HSV = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        oldHSV = np.copy(HSV)
        sred = 0
        count = 0
        for item in HSV:
            for pixel in item:
                sred = sred + pixel[1]
                count = count +1
        sred = sred / count
        if (sred<150):
            sred = 170
        for item in HSV:
            for pixel in item:
                if pixel[1] > (sred):
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255
                else:
                    pixel[0] = 0
                    pixel[1] = 0
        newgray = cv2.cvtColor(HSV, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, 200, 255, cv2.THRESH_BINARY)
        # Поиск границ для нового фото.
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cont,_ = PreProcessPhoto._findBiggestCountour(contours)
        approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
        cv2.drawContours(image,approx,-1,(255,0,0), 5)
        cv2.drawContours(image,cont,-1,(0,255,0), 5)
        Otladka.ShowImages([image, oldHSV, HSV, binary])
        return cont

    def FindDocOtladka(pathorimage) -> np.ndarray: # Работающий метод
        # image = PreProcessPhoto.FindRectangle(pathorimage)
        # image = cv2.imread(pathorimage)
        cont = PreProcessPhoto._findContour(pathorimage)
        # approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
        # (p1,p1i) = PreProcessPhoto._findpoint(approx[0][0][0],approx[0][0][1],cont)
        # (p2,p2i) = PreProcessPhoto._findpoint(approx[1][0][0],approx[1][0][1],cont)
        # (p3,p3i) = PreProcessPhoto._findpoint(approx[2][0][0],approx[2][0][1],cont)
        # (p4,p4i) = PreProcessPhoto._findpoint(approx[3][0][0],approx[3][0][1],cont)
        # newindexes = [p1i,p2i,p3i,p4i]
        # oldindexes = newindexes.copy()
        # points = [p1,p2,p3,p4]
        # newindexes.sort()
        # for item in oldindexes:
        #     if (item == newindexes[0]):
        #         newp1 = points[oldindexes.index(item)]
        #     if (item == newindexes[1]):
        #         newp2 = points[oldindexes.index(item)]
        #     if (item == newindexes[2]):
        #         newp3 = points[oldindexes.index(item)]
        #     if (item == newindexes[3]):
        #         newp4 = points[oldindexes.index(item)]
        # cv2.line(image,newp1,newp2, (0,0,255), 5)
        # cv2.line(image,newp2,newp3, (0,0,255), 5)
        # cv2.line(image,newp3,newp4, (0,0,255), 5)
        # cv2.line(image,newp4,newp1, (0,0,255), 5)
        # cv2.drawContours(image, cont,-1, (255,0,0), 5)
        # Otladka.ShowImages([image])
        # vs1 = cont[newindexes[newindexes.index(p1i)]+1][0]
        # vs2 = cont[newindexes.index(p2i)][0]
        # vs3 = cont[indexes.index(p3i)][0]
        # vs4 = cont[indexes.index(p4i)][0]
        # cv2.line(image,newp1,vs1, (0,0,255), 5)
        # Otladka.ShowImages([image])
        # x3  =image.shape[1]+10
        # y3 = PreProcessPhoto.line_equation(p5[0], p5[1], p4[0], p4[1], x3)
        # p = np.copy(p5)
        # p[0] = x3
        # p[1] = y3
        # cv2.line(image,p5,p, (0,0,255), 5)
        
        # y2 = image.shape[0]+10
        # x2 = PreProcessPhoto.line_equation2(p2[0], p2[1], p3[0], p3[1], y2)
        # p0 = np.copy(p5)
        # p0[0] = x2
        # p0[1] = y2
        # cv2.line(image,p2,p0, (0,0,255), 5)
        # Otladka.ShowImages([image])
        # pt_A = p1
        # pt_B = p2
        # pt_D = p5
        # pt_C = 
        # width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
        # width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
        # maxWidth = max(int(width_AD), int(width_BC))
        # height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
        # height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
        # maxHeight = max(int(height_AB), int(height_CD))
        # input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
        # output_pts = np.float32([[ 0,0],
        #                         [0, maxHeight - 1],
        #                         [maxWidth - 1, maxHeight - 1],
        #                         [maxWidth - 1, 0]])
        # M =  cv2.getPerspectiveTransform(input_pts,output_pts)
        # Otladka.ShowImages([cv2.warpPerspective(image,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)])
    def _findpoint(x:int,y:int, cont:np.ndarray):
        for i in range(0,len(cont)):
            if (cont[i][0][0] == x and cont[i][0][1] == y):
                return (cont[i][0], i)
    def line_equation(x1, y1, x2, y2, x):
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return k*x + b
    def line_equation2(x1, y1, x2, y2, y):
        if (y2==y1):
            y2 = y2+1
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return (y-b)/k
    # def findintersec(x1,k1,b1,x2,k2,b2):
        
        
    def _GetPerspectiveTransform(approx:np.ndarray, image:np.ndarray) -> np.ndarray: # Обрезка изображения по контуру.
        # Поворот точек контура.
        if PreProcessPhoto._FindPointsToRotate(approx) is None:
            return None
        (pt_A, pt_B, pt_C, pt_D) = PreProcessPhoto._FindPointsToRotate(approx)
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
    
    def GetPreprocessPhotoOtladka():
        root = tk.Tk()
        root.withdraw()  # скрываем главное окно
        file_path = filedialog.askopenfilename()  # вызываем диалоговое окно
        PreProcessPhoto.FindDocOtladka(file_path)

class PreProcessPhotov2():
    def __init__(self, pix1=100, pix0=20, thresh=150):
        self.thresh = thresh
        self.pix0 = pix0
        self.pix1 = pix1
    def SetValues(self, pix1=100, pix0=20, thresh=150):
        self.thresh = thresh
        self.pix0 = pix0
        self.pix1 = pix1
    def OpenImage(pathorimage):
        if (type(pathorimage) == str):
            image = cv2.imread(pathorimage)
        elif (type(pathorimage) == np.ndarray):
            image = pathorimage
        else:
            raise Exception("Неправильный тип данных")
        return image
    def Work(self,pathorimage):
        image = PreProcessPhotov2.OpenImage(pathorimage) # Открытие изображения.
        cropimage = np.copy(image);
        cropimage = cv2.cvtColor(cropimage, cv2.COLOR_RGB2BGR)
        i = 0
        binary =0
        approx = [0]
        while len(approx) != 4: 
            if i > 12:
                return None
            if i == 0:
                cropimage = cv2.cvtColor(cropimage, cv2.COLOR_BGR2RGB)
            i = i + 1
            image = np.copy(cropimage)
            # Otladka.ShowImages([image, cropimage])
            HLSimage = PreProcessPhotov2.HLS(image) # HLS - по "светлоте фото"
            binary = HLSimage
            if HLSimage is None:
                HSVimage = PreProcessPhotov2.HSV(image) # HSV - по " значеию цвета"
                binary = HSVimage
                if HSVimage is None:
                    grayImage = PreProcessPhotov2.gray(image) # Без обработки
                    binary = grayImage
                    cropimage, approx = PreProcessPhotov2.CropContour(image, binary)
                else:
                    cropimage, approx = PreProcessPhotov2.CropContour(image, binary)
            else: 
                cropimage, approx = PreProcessPhotov2.CropContour(image, binary)
        cropimage = PreProcessPhotov2.WhitePhon(image, binary)
        ret = PreProcessPhotov2.ApproxImage(approx,cropimage)
        print(i)
        return [ret]
    def HLS(image):
        copy = np.copy(image)
        HLS = cv2.cvtColor(copy, cv2.COLOR_RGB2HLS_FULL)
        sredLight1= 0
        count = 0
        for item in HLS:
            for pixel in item:
                sredLight1= sredLight1 + pixel[1]
                count = count +1
        sredLight1 = sredLight1 / count
        print("Ligthness", str(sredLight1))
        if sredLight1 < 50 or sredLight1>115:
            return None
        sredLight= 0
        count = 0
        # Otladka.ShowImages([HLS])
        for item in HLS:
            for pixel in item:
                if pixel[1] > sredLight1:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255                  
                else:
                    count =count +1 
                    sredLight = sredLight + pixel[1]
                    pixel[0] = 0
                    pixel[2] = 0
        sredLight = sredLight / count
        print("Ligthness", str(sredLight))
        if sredLight*2 > sredLight1:
            return None
        # Otladka.ShowImages([HLS])
        for item in HLS:
            for pixel in item:
                if pixel[1] > sredLight1 - sredLight/2.5:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255 
                else: 
                    pixel[0] = 0
                    pixel[1] = 0
                    pixel[2] = 0
        newgray = cv2.cvtColor(HLS, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(newgray, 200, 255, cv2.THRESH_BINARY)
        # Otladka.ShowImages([binary])
        return binary
    def HSV(image):
        copy = np.copy(image)
        HSV = cv2.cvtColor(copy, cv2.COLOR_RGB2HSV_FULL)
        
        sredVal= 0
        sredSat= 0
        count = 0
        for item in HSV:
            for pixel in item:
                sredVal= sredVal + pixel[2]
                sredSat = sredSat + pixel[1]
                count = count +1
        sredVal = sredVal / count
        sredSat = sredSat / count
        print("Value", str(sredVal), "Saturation", str(sredSat))
        if sredSat > 50:
            return None
        # Otladka.ShowImages([HSV])
        for item in HSV:
            for pixel in item:   
                if pixel[1] < sredSat and pixel[2] > sredVal/1.2:
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
        # Otladka.ShowImages([binary])
        return binary
    def gray(image):
        copy = np.copy(image)
        newgray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
        sred= 0
        count = 0
        for item in newgray:
            for pixel in item:
                sred= sred + pixel
                count = count +1
        sred = sred / count
        print("gray", str(sred))
        _, binary = cv2.threshold(newgray, 175, 255, cv2.THRESH_BINARY)
        return binary
    def CropContour(image, binary):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))  
        opening = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        dilated = cv2.dilate(opening, kernel, iterations=3)
        
        # newgray = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)
        # _, bina = cv2.threshold(newgray, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key = cv2.contourArea)

        approx = cv2.approxPolyDP(contour, 0.049 * cv2.arcLength(contour, True), True)

        x, y, w, h = cv2.boundingRect(approx)
        # Crop the image
        cropped_img = image[y: y + h, x: x + w]
        # cv2.drawContours(image,[approx],-1, (255,0,0), 5)
        # Otladka.ShowImages([image])

        return cropped_img, approx
    def WhitePhon(image, binary):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))  
        opening = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        dilated = cv2.dilate(opening, kernel, iterations=3)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key = cv2.contourArea)
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], -1, (255,255,255), -1)
        out = np.ones_like(image)
        out = 255*out
        out[mask == 255] = image[mask == 255]
        out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
        return out
    def ApproxImage(approx,image):      
        # cv2.drawContours(image,[approx],-1, (255,0,0), 5)
        # Otladka.ShowImages([image])
        return PreProcessPhoto._GetPerspectiveTransform(approx, image)
        
        







