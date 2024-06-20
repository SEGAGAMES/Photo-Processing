#!/usr/bin/python
# -*- coding: cp1251  -*-
import speech_recognition as sr
class SpeechRecognizer():
    def GetVoice():
        r = sr.Recognizer()
        with sr.Microphone() as audioSource:
            r.adjust_for_ambient_noise(audioSource, duration=0.5)
            return r.listen(audioSource, phrase_time_limit=20)
    def Recognize(audio):
        r=sr.Recognizer() 
        r.pause_threshold = 0.2
        try:
            text = r.recognize_google(audio, language = "ru-RU")
            f = open("C:\Works\speechrecognizeresult.txt", 'a')
            f.write(text + " ")
            f.close()
        except sr.UnknownValueError:
            return     
    def recognise(filename):
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text,language="ru-RU")
                return text
            except:
                print('Sorry.. run again...')
                return "Sorry.. run again..."

