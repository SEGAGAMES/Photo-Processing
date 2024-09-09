#!/usr/bin/python
# -*- coding: cp1251  -*-
import easyocr
class TextReader():
    def ReadText(image_or_path, language:str = 'ru'):
        reader = easyocr.Reader(language.split(), gpu=False,model_storage_directory='EasyOCR/model',verbose = False)
        # reader = easyocr.Reader(['en'],
        #                 model_storage_directory='custom_EasyOCR/model',
        #                 user_network_directory='custom_EasyOCR/user_network',
        #                 recog_network='custom_example') 
        result = reader.readtext(image_or_path, detail = 0, paragraph=True)#, contrast_ths=0.5,slope_ths=0.5, y_ths =1, x_ths = 1, width_ths=0.1,height_ths=0.1, min_size=2) 
        return result
        
                