#!/usr/bin/python
# -*- coding: cp1251  -*-
import cv2
import numpy as np
# import easyocr

def findbiggest(cont):
    maxx = cont[0]
    for item in cont:
        if (cv2.contourArea(item) > cv2.contourArea(maxx)):
            maxx = item
    return maxx

def Work(path):
    
    image = cv2.imread(path)
    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray)
    plt.show()
    
    ret, binary = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = findbiggest(contours)        
    img_copy = np.copy(image)
    img_copy = cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)
    img_copy = cv2.drawContours(img_copy, [cont], -1, (0, 0, 255), 2)
    approx = cv2.approxPolyDP(cont, 0.045 * cv2.arcLength(cont, True), True)
    img_copy = cv2.drawContours(img_copy, [approx], -1, (0, 255, 255), 2)
    plt.imshow(img_copy)
    plt.show()
    
    if (len(approx) == 4):
        pt_A = approx[0][0]
        pt_B = approx[1][0]
        pt_C = approx[2][0]
        pt_D = approx[3][0]
    else:
        return [None]
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
    plt.imshow(outImage)
    plt.show()
    return outImage 




def text_recognition(file_path, language):
    try:
        reader = easyocr.Reader(language.split())
        result = reader.readtext(file_path, detail = 0, paragraph=True) 
        return result
    except:
        return 0
def OpenFile(path):
    try:
        f = open(path,encoding="utf8 ")
        return f.read()
    except:
        return 0
def recognize(image, languages):
    result = []
    for item in text_recognition(image, language=languages): 
            result.append(item)
    return result
def main():
    f = open("C:\Works\log.txt", 'w')
    f.write("start")
    f.close
    f= open("C:\Works\photorecognizeresult.txt", 'w')
    f.close()
    pathes = OpenFile("C:\Works\Filenames.txt")
    languages = OpenFile("C:\Works\languages.txt")
    if (languages!= 0 and pathes != 0):
        for path in pathes.split(">"):
            if (path != ""):
                 image = Work(path) 
                 if (image.all() == None):
                    continue
                 f = open("C:\Works\photorecognizeresult.txt", 'a', encoding="utf-8")
                 try:
                     for item in recognize(image, languages):
                        f.write("%s\n" % item) 
                 finally:
                    f.close()
    f = open("C:\Works\log.txt", 'w')
    f.write("end")
    f.close
main()

    

