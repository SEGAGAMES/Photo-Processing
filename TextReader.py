import easyocr
class TextReader():
    def ReadText(image_or_path, language:str = 'ru en'):
        reader = easyocr.Reader(language.split(), gpu=False)
        result = reader.readtext(image_or_path,batch_size = 10, detail = 0, paragraph=True, contrast_ths=0.5,slope_ths=0.5, ycenter_ths =0.1, width_ths=0.1,height_ths=0.1, min_size=2) 
        return result
        
                