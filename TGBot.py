#!/usr/bin/python
# -*- coding: cp1251  -*-
from PreProcessPhoto import PreProcessPhotov2
import telebot;
from telebot import types
import cv2;
import threading 
import os 
from threading import Lock
from TextReader import TextReader   #   pip install pysoundfile



bot = telebot.TeleBot('6817178987:AAGbWfjbW9_GDZxSmQO-oloJPrj6_yHQxzM')
resize_data = {}
lock = Lock()
@bot.message_handler(content_types=['text'])  
def get_text_messages(message): # Работа с сообщениями
    if message.text == "Поиск документа":
        bot.send_message(message.from_user.id, "Отправьте фото для поиска")
        resize_data[message.from_user.id] = "Обрезка"
    elif message.text == "Распознавание текста":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Русский")
        btn2 = types.KeyboardButton("Английский и русский")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выберите опцию", reply_markup=markup)
        bot.send_message(message.from_user.id, "Отправьте фото для распознавания (ТОЛЬКО РУССКИЙ)")
        resize_data[message.from_user.id] = "Только распознавание"
    elif message.text == "Поиск и распознавание текста":
        pass
    elif message.text == "Русский":
        
        pass
    elif message.text == "Английский и русский":
        pass
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Поиск документа")
        btn2 = types.KeyboardButton("Распознавание текста")
        btn3 = types.KeyboardButton("Поиск и распознавание текста")
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, text="Выберите опцию", reply_markup=markup)
        
@bot.message_handler(content_types=['photo'])
def photo(message):
    t1 = threading.Thread(target=Work, args =(message,))
    t1.start()
def Work(message):
    # Сохранение фото.
    (bot.send_message(message.chat.id, text="Обработка...")) 
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("temp" + str(message.id) +".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Значение по умолчанию.
    if message.from_user.id not in resize_data:
        resize_data[message.from_user.id] = True
        
    # Обработка фото.
    photos = PreProcessPhotov2.Work("temp" + str(message.id) +".jpg")  
    # Фото не найдено.
    if photos is None or photos[0] is None:
        bot.send_message(message.chat.id, text="Документы не найдены")
        return
    # Работа с фото, распознавание или просто вывод.
    elif  resize_data[message.from_user.id] == False:
        cv2.imwrite("temp" + str(message.id) +".jpg",photos[0])
        img = open("temp" + str(message.id) +".jpg", 'rb')
        text = TextReader.ReadText(photos[1])
        lock.acquire()
        bot.send_photo(message.from_user.id, img)
        img.close()
        bot.send_message(message.chat.id, text=text)
        lock.release()
        os.remove("temp" + str(message.id) +".jpg")
        return
    else:
        cv2.imwrite("temp" + str(message.id) +".jpg",photos[0])
        img = open("temp" + str(message.id) +".jpg", 'rb')
        bot.send_photo(message.from_user.id, img)
        img.close()
        os.remove("temp" + str(message.id) +".jpg")
        return

print("Start...")
bot.polling(none_stop=True, interval=0)

 


