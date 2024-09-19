#!/usr/bin/python
# -*- coding: cp1251  -*-
import easyocr
from SpellCheck import WordWork
class TextReader():
    def ReadText(image_or_path, russian = True, noLetters = True):
        if noLetters:
            reader = easyocr.Reader(["en"], verbose=False, gpu=False)
            result = reader.readtext(image_or_path, detail = 0, paragraph=False)
            text = ""
            for item in result:
                text = text + " " + item
            text = text.replace('.', ':')
            return text
        if not russian:
            reader = easyocr.Reader(["ru", "en"], verbose=False, gpu=False)
            result = reader.readtext(image_or_path, detail = 0, paragraph=True)
            letters = "abdfgijknlmopqrstuywz"
            for item in result:
                for letter in letters:
                    if letter not in item.lower():
                        continue
                    else:
                        return result
        else:
            reader = easyocr.Reader(["ru"], gpu=False,model_storage_directory='EasyOCR/model',verbose = False)
            result = reader.readtext(image_or_path, detail = 0, paragraph=True)#, contrast_ths=0.5,slope_ths=0.5, y_ths =1, x_ths = 1, width_ths=0.1,height_ths=0.1, min_size=2) 
            text = ""
            for item in result:
                text = text + " " + item
            result = WordWork.FindSame(text)
            if result is None or len(result)==1 or len(result) == 0:
                return text
            return result
        
                