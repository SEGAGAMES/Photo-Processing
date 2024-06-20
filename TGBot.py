#!/usr/bin/python
# -*- coding: cp1251  -*-
from email.headerregistry import ContentDispositionHeader
from ImageUpdate import ImageUpdate
from PreProcessPhoto import PreProcessPhotov2
from SpeechRecognizer import SpeechRecognizer
import telebot;
from telebot import types
import cv2;
import threading 
import os 
import soundfile as sf

from TextReader import TextReader   #   pip install pysoundfile



bot = telebot.TeleBot('6817178987:AAGbWfjbW9_GDZxSmQO-oloJPrj6_yHQxzM');
PreProcess = True
@bot.message_handler(content_types=['text'])  
def get_text_messages(message): # Работа с сообщениями
    if message.text == "Поиск документа":
        print("text with: " + str(message.from_user.id))
        bot.send_message(message.from_user.id, "Отправьте фото для обрезки P.S. Оберзаем фото документов на фоне другого цвета..")
        img = open("example.jpg", 'rb')
        bot.send_photo(message.from_user.id, img, caption='Например,')
        PreProcess = True
    elif message.text == "Распознавание текста":
        print("text with: " + str(message.from_user.id))
        bot.send_message(message.from_user.id, "Отправьте фото для распознавания")
        PreProcess = False
        print()
    else:
        print("start with: " + str(message.from_user.id))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Поиск документа")
        btn2 = types.KeyboardButton("Распознавание текста")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выбери опцию", reply_markup=markup)
        
@bot.message_handler(content_types=['photo'])
def photo(message):
    if PreProcess == True:
        ph = threading.Thread(target = Work, args = (message,)) # Для реализации многопоточности 2 метода.
        ph.start()
    else:
         bot.send_message(message.from_user.id, "еще не робит..")
def Work(message): # Работа с фото.
    print("photo from: " + str(message.from_user.id))
    bot.send_message(message.chat.id, text="Обработка...")
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("temp" + str(message.from_user.id) +".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    # text = TextReader.ReadText("temp" + str(message.from_user.id) +".jpg")
    # for item in text:
    #     bot.send_message(message.chat.id, text=item)
    photos = PreProcessPhotov2.Work("temp" + str(message.from_user.id) +".jpg")
    if photos is None:
        bot.send_message(message.chat.id, text="Документы не найдены")
        return
    # photos = ImageUpdate.Update(photos)
    if len(photos) == 1:
        cv2.imwrite("temp" + str(message.from_user.id) +".jpg",photos[0])
        img = open("temp" + str(message.from_user.id) +".jpg", 'rb')
        try:
            bot.send_photo(message.from_user.id, img)
            text = TextReader.ReadText("temp" + str(message.from_user.id) +".jpg")
            for item in text:
                bot.send_message(message.chat.id, text=item)
        except:
            bot.send_message(message.chat.id, text="Ошибка отправки")
            print('ошибка отправки с  ' + str(message.from_user.id))
        img.close()
        print('Отправлено ' + str(message.from_user.id))
        os.remove("temp" + str(message.from_user.id) +".jpg")
        return
    else:
        for item in photos:
            if item is None :
                continue
            cv2.imwrite("temp" + str(message.from_user.id) +".jpg",item)
            img = open("temp" + str(message.from_user.id) +".jpg", 'rb')
            try:
                # bot.send_message(message.chat.id, text=TextReader.ReadText("temp" + str(message.from_user.id) +".jpg"))
                bot.send_photo(message.from_user.id, img)
            except:
                bot.send_message(message.chat.id, text="Ошибка отправки")
                print('ошибка отправки с  ' + str(message.from_user.id))
            img.close()
            print('Отправлено ' + str(message.from_user.id))
            os.remove("temp" + str(message.from_user.id) +".jpg")
    return

@bot.message_handler(content_types=['voice'])
def voice_to_text(message):

    file_name_full="temp"+str(message.from_user.id)+".ogg"
    file_name_full_converted="tempready"+str(message.from_user.id)+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    data, samplerate = sf.read(file_name_full)
    sf.write(file_name_full_converted, data, samplerate)
    text=SpeechRecognizer.recognise(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
print("Start...")
bot.polling(none_stop=True, interval=0)

 


