import easyocr
class TextReader():
    def ReadText(image_or_path, language:str = 'ru'):
        reader = easyocr.Reader(language.split())
        result = reader.readtext(image_or_path, detail = 0, paragraph=True) 
        return result
        
                