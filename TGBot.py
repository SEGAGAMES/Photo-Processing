#!/usr/bin/python
# -*- coding: cp1251  -*-
from PreProcessPhoto import PreProcessPhoto
import telebot;
from telebot import types
import cv2;
import threading 
import os 

bot = telebot.TeleBot('6817178987:AAGbWfjbW9_GDZxSmQO-oloJPrj6_yHQxzM');
PreProcess = True

@bot.message_handler(content_types=['text'])  
def get_text_messages(message):
    
    if message.text == "Обрезка фото":
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
        btn1 = types.KeyboardButton("Обрезка фото")
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
def Work(message):
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("temp" + str(message.from_user.id) +".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    photos = PreProcessPhoto.GetBestPhotos("temp" + str(message.from_user.id) +".jpg")
    for item in photos:
        cv2.imwrite("temp" + str(message.from_user.id) +".jpg",item)
        img = open("temp" + str(message.from_user.id) +".jpg", 'rb')
        bot.send_photo(message.from_user.id, img)
        img.close()
        print('Отправлено ' + str(message.from_user.id))
        os.remove("temp" + str(message.from_user.id) +".jpg")
print("Start...")
bot.polling(none_stop=True, interval=0)

 


