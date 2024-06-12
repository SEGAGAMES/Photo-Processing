#!/usr/bin/python
# -*- coding: cp1251  -*-
from os import replace
import string
from tkinter.messagebox import RETRY
from tkinter.tix import MAX


letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
class TextWork():
    def OpenText(path, encoding = None):
        if (encoding == None):
            f = open(path, 'r')
            text = f.readlines()
            f.close()
            return text
        else:
            f = open(path, 'r', encoding=encoding)
            text = f.readlines()
            f.close()
            return text
        
    def PreprocessText(text):
        newtext= ""
        for line in text:
            newline = ""
            for word in line.split():
                newword = ""
                for letter in word.lower():
                    if (letter in letters):
                        newword = newword+letter
                newline = newline + " " + newword
            newtext = newtext + "%s\n" % newline
        return newtext
    
    def ReplaseBad2Good(badWords, goodWords, openText):
        textLower = []
        for line in openText:
            textLower.append(line.lower())
        for i in range(len(badWords)):
            for line in textLower:
                if (badWords[i] in line):
                    index = textLower.index(line)
                    line = line.replace(badWords[i], goodWords[i])
                    textLower[index] = line
        return textLower
    
    def SaveText(path,text:string):
        f = open(path, 'w', encoding="utf-8")
        f.write(text)
        f.close()
    def SaveText(path,text:list):
        f = open(path, 'w', encoding="utf-8")
        for item in text:
            f.write(item)
        f.close()
class WordWork():
    def BadWord(word):
        path = "C:\\Works\\Dictionares\\" + str(len(word)) + ".txt"
        dictionary = TextWork.OpenText(path, "utf-8")
        word = word + "\n"
        if (word not in dictionary):
            return True
        else:
            return False
        
    def FindBadWords(PreprocessedText):
        result = []
        for word in PreprocessedText.split():
            if (WordWork.BadWord(word)):
                result.append(word)
            else:
                continue
        return result
    
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
        if (len(breakSymbols)-1 <= len(word1) // 3):
            return len(breakSymbols)-1
        else:
            return -1
        
    def FindSame(word):
        path = "C:\\Works\\Dictionares\\" + str(len(word)) + ".txt"
        dictionary = TextWork.OpenText(path, "utf-8")
        result = []
        word = word
        error = []
        result2 = []
        for line in dictionary:
            word2 = line.split()[0]
            errors = WordWork.SameString(word, word2)
            if errors == 1:
                return [word2]
            if (errors <= len(word) // 3 and errors != -1):
                error.append(errors)
                result.append(word2)
        # Сохранение в порядке ошибок
        for i in range(len(result)):
            if (error[i] == 1):
                result2.append(result[i])
        for i in range(len(result)):
            if (error[i] == 2):
                result2.append(result[i])
        for i in range(len(result)):
            if (error[i] == 3):
                result2.append(result[i])
        return result2
    
    def CreateGood(badWords):
        goodWords = []
        for badWord in badWords:
            good = WordWork.FindSame(badWord)
            if (len(good) > 0):
                goodWords.append(good[0])
            else:
                goodWords.append(badWord)
        return goodWords
    
class TextProcesser():
    def ProcessText(textPath, newTextPath):
        openText = TextWork.OpenText(textPath, "utf-8")
        preprocessedText = TextWork.PreprocessText(openText)
        badWords = WordWork.FindBadWords(preprocessedText)
        goodWords = WordWork.CreateGood(badWords)
        newText = TextWork.ReplaseBad2Good(badWords, goodWords, openText)
        TextWork.SaveText(newTextPath, newText)
class Dict():
    def DelDuplicates(path):
        text = TextWork.OpenText(path, "utf-8")
        st = set(text)
        text = list(st)
        TextWork.SaveText(path, text)
    def ClearDict():
        mainDict = TextWork.OpenText("C:\\Works\\RUS.txt")
        newDict = []
        bol = True
        for line in mainDict:
            word = line
            for item in word:
                if (item != "\n"):
                    if (item not in letters):
                        bol = False
                        continue
            if (bol == True):
                newDict.append(word)
            else:
                bol = True
        TextWork.SaveText("C:\\Works\\new_RUS.txt", newDict)
    def CreateDicts():
        mainDict = TextWork.OpenText("C:\\Works\\new_RUS.txt", "utf-8")
        maxLen = 0
        for line in mainDict:
            word = line
            if (len(word) > maxLen):
                maxLen = len(word)
                if (maxLen == 26):
                    print(word)
        print(maxLen)
    
        for textLen in range(maxLen):
            textLen = textLen + 2
            oneLenWords = []
            for line in mainDict:
                word = line
                if (len(word) == textLen):
                    oneLenWords.append(word)
            TextWork.SaveText("C:\\Works\\Dictionares\\" + str(textLen-1) + ".txt", oneLenWords)
# Dict.CreateDicts()
# TextProcesser.ProcessText("C:\\Works\\temp.txt", "C:\\Works\\temp.txt")