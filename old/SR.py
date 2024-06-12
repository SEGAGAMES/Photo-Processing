#!/usr/bin/python
# -*- coding: cp1251  -*-
import threading 
import speech_recognition
def GetVoice():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as audioSource:
        r.adjust_for_ambient_noise(audioSource, duration=0.5)
        return r.listen(audioSource, phrase_time_limit=20)
def Recognize(audio):
    import speech_recognition as sr 
    r=sr.Recognizer() 
    r.pause_threshold = 0.2
    try:
        text = r.recognize_google(audio, language = "ru-RU")
        f = open("C:\Works\speechrecognizeresult.txt", 'a')
        f.write(text + " ")
        f.close()
    except sr.UnknownValueError:
        return
def Work():
    audio = GetVoice()
    recognize = threading.Thread(target = Recognize, args = (audio,))
    recognize.start()        
if __name__ == "__main__":
    while (True):  
        Work()

