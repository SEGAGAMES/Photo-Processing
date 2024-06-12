#!/usr/bin/python
# -*- coding: cp1251  -*-
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2
from collections import Counter

# from corus import load_lenta

# path = "D:\Учеба\проект 5 курс\питон\lenta-ru-news.csv.gz"
# records = load_lenta(path)
# for record in records:
#     print(record.text)
#     break
# nltk.download('stopwords')
# nltk.download('punkt')
stop_words = stopwords.words("russian")
punkt_symbols = ['!', '.', ',', '?', '-','']
bad_words = ['ебать', 'ёбаный рот', 'сука', 'хулить', 'блядь',]
morph = pymorphy2.MorphAnalyzer()
def OpenFile(path):
    with open(path, "r", encoding="UTF-8") as f:
        text = f.read()
        text = text.replace("\n", " ")
    return text
def SaveFile(path, text):
    f = open(path, 'w', encoding="UTF-8")
    for item in text:
        f.write(item+"\n")
def preprod(text):
    tokens = word_tokenize(text.lower())
    new_tokens = []
    for token in tokens:
        if (token not in punkt_symbols):
            if (morph.parse(token)[0].is_known == True):
                new_tokens.append(token)                  
    return new_tokens
def Freq(tokens):
    test_counter = Counter(tokens)
    print(test_counter.most_common(5))
# summ = 0
# for i in range(1,26):
#     path = "C:\\Works\\Dictionares\\" + str(i) + ".txt"
#     text = OpenFile(path)
#     tokens = preprod(text)
#     text = text.split()
#     l = len(text)-len(tokens)
#     summ = summ+l
#     print(l)
#     SaveFile(path, tokens)
# print(summ)
# print(morph.parse("стен")[0].normal_form)