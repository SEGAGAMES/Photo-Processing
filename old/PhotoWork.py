#!/usr/bin/python
# -*- coding: cp1251  -*-
import cv2
import numpy as np
# import easyocr
def Otladka(image):
    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()
class PreProcess():
    def Findbiggest(cont):
        maxx = cont[0]
        for item in cont:
            if (cv2.contourArea(item) > cv2.contourArea(maxx)):
                maxx = item
        return maxx
    def Find(path:str, thresh:int=150, step:int=5) -> []:
        ans = PreProcess.TryContour(path,thresh)
        if (len(ans) != 1):
            return ans
        else:
            i = thresh
            while i - step > 130:
                i = i-step
                ans = PreProcess.TryContour(path,i)
                if (len(ans) != 1):
                    return [ans]
            i = thresh
            while i + step < 180:
                i = i +step
                ans = PreProcess.TryContour(path,i)
                if (len(ans) != 1):
                    return [ans]
    def TryContour(path:str, thresh:int=150) -> []:
        image = cv2.imread(path)
        # Otladka(image)
    
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Otladka(gray)
    
        ret, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont = PreProcess.Findbiggest(contours)        
        img_copy = np.copy(image)
        img_copy = cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)
        img_copy = cv2.drawContours(img_copy, [cont], -1, (0, 0, 255), 2)
        approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
        img_copy = cv2.drawContours(img_copy, [approx], -1, (0, 255, 255), 2)
        # Otladka(img_copy)
    
        if (len(approx) == 4):
            pt_A = approx[0][0]
            pt_B = approx[1][0]
            pt_C = approx[2][0]
            pt_D = approx[3][0]
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
            M = cv2.getPerspectiveTransform(input_pts,output_pts)
            outImage = cv2.warpPerspective(image,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
            Otladka(outImage)
            return outImage
        else:
            return [0]
PreProcess.Find("D:\\1.jpg");



