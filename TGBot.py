#!/usr/bin/python
# -*- coding: cp1251  -*-
from PreProcessPhoto import PreProcessPhoto
import telebot;
import cv2;
import threading 
import os 
bot = telebot.TeleBot('6817178987:AAGbWfjbW9_GDZxSmQO-oloJPrj6_yHQxzM');
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Обрезать фото и")
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, отправь фото")
@bot.message_handler(content_types=['photo'])
def photo(message):
    ph = threading.Thread(target = Work, args = (message,))
    ph.start()
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
bot.polling(none_stop=True, interval=0)

 


