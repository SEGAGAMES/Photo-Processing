#!/usr/bin/python
# -*- coding: cp1251  -*-
from ImageUpdate import ImageUpdate
from PreProcessPhoto import Otladka, PreProcessPhoto, PreProcessPhotov2
import telebot;
from telebot import types
import cv2;
import threading 
import os 

bot = telebot.TeleBot('6817178987:AAGbWfjbW9_GDZxSmQO-oloJPrj6_yHQxzM');
PreProcess = True
PreProcesser = PreProcessPhotov2()
@bot.message_handler(content_types=['text'])  
def get_text_messages(message): # Работа с сообщениями
    if "thresh" in message.text:
        PreProcesser.SetValues(pix1=PreProcesser.pix1, pix0 = PreProcesser.pix0,thresh=int(message.text.split()[1]))
        print("set value thresh in " + message.text.split()[1])
        return
    if "pix0" in message.text:
        PreProcesser.SetValues(pix0=int(message.text.split()[1]), pix1=PreProcesser.pix1, thresh=PreProcesser.thresh)
        print("set value pix0 in " + message.text.split()[1])
        return
    if "pix1" in message.text:
        PreProcesser.SetValues(pix1=int(message.text.split()[1]), pix0 = PreProcesser.pix0, thresh=PreProcesser.thresh)
        print("set value pix1 in " + message.text.split()[1])
        return
    if "Values" == message.text:
        print(str(PreProcesser.pix0), str(PreProcesser.pix1), str(PreProcesser.thresh)) 
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
    photos = PreProcesser.Work("temp" + str(message.from_user.id) +".jpg")
    if photos is None:
        bot.send_message(message.chat.id, text="Документы не найдены")
        return
    # photos = ImageUpdate.Update(photos)
    if len(photos) == 1:
        cv2.imwrite("temp" + str(message.from_user.id) +".jpg",photos[0])
        img = open("temp" + str(message.from_user.id) +".jpg", 'rb')
        try:
            bot.send_photo(message.from_user.id, img)
        except:
            bot.send_message(message.chat.id, text="Ошибка отправки")
            print('ошибка отправки с  ' + str(message.from_user.id))
        img.close()
        print('Отправлено ' + str(message.from_user.id))
        os.remove("temp" + str(message.from_user.id) +".jpg")
        return
    else:
        for item in photos:
            cv2.imwrite("temp" + str(message.from_user.id) +".jpg",item)
            img = open("temp" + str(message.from_user.id) +".jpg", 'rb')
            try:
                bot.send_photo(message.from_user.id, img)
            except:
                bot.send_message(message.chat.id, text="Ошибка отправки")
                print('ошибка отправки с  ' + str(message.from_user.id))
            img.close()
            print('Отправлено ' + str(message.from_user.id))
            os.remove("temp" + str(message.from_user.id) +".jpg")
    return
print("Start...")
bot.polling(none_stop=True, interval=0)

 


