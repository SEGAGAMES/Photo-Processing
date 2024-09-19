#!/usr/bin/python
# -*- coding: cp1251  -*-
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2
from collections import Counter

class WordWork():
    def SameString(word1, word2):
        if (len(word2) != len(word1)):
            return -1
        breakSymbols = [0]
        for subStringLen in range(len(word1) +1):
            substringa = word1[breakSymbols[-1]:subStringLen]
            substringab = word2[breakSymbols[-1]:subStringLen]
            if (substringa == substringab):
                continue
            else:
                breakSymbols.append(subStringLen)
        one = len(breakSymbols)-1
        two = len(word1) // 3
        if (len(word1) < 3):
            two = two + 1
        if (one  <= two):
            return len(breakSymbols)-1
        else:
            return -1
    def preprod(text):
        stop_words = stopwords.words("russian")
        punkt_symbols = ['!', '.', ',', '?', '-',':', ";", '\'', '_',]
        bad_words = ['ебать', 'ёбаный рот', 'сука', 'хулить', 'блядь',]
        morph = pymorphy2.MorphAnalyzer()
        tokens = word_tokenize(text.lower())
        new_tokens = []
        for token in tokens:
            if (token not in punkt_symbols):
                for symb in token:
                    if symb in punkt_symbols:
                        token = token.replace(symb,"")
                new_tokens.append(token)                  
        return new_tokens
    def FindSame(text):
        tokens = WordWork.preprod(text)
        if len(tokens) == 0:
            return
        text = ""
        numbers = ['0', '1', '2','3','4','5','6','7','8','9',]        
        for word in tokens:
            brea = False
            for symb in word:
                if symb in numbers:
                    brea = True
            if brea == True:
                continue
            path = "C:\\Works\\Dictionares\\" + str(len(word)) + ".txt"
            f = open(path, 'r', encoding="UTF-8")
            dictionary = f.readlines()
            f.close()
            result = []
            error = []
            result2 = []
            for line in dictionary:
                word2 = line.split()[0]
                errors = WordWork.SameString(word, word2)
                if errors == 1:
                    error.append(errors)
                    result.append(word2)
                elif (errors <= len(word) // 3 and errors != -1):
                    error.append(errors)
                    result.append(word2)
                    if errors == 0:
                        break
            if len(result) == 0:
                text = text + word + " "
                break
            minim = 10
            for i in error:
                if i <minim:
                    minim = i
                    minindex = error.index(i)
            text = text + result[minindex] + " "
        return text
