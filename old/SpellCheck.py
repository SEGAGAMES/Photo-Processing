#!/usr/bin/python
# -*- coding: cp1251  -*-
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
        
    def FindSame():
        f = open("C:\\Works\\log\\tempText.txt", 'r', encoding="UTF-8")
        word = f.readline()
        f.close()
        if len(word) == 0:
            return
        path = "C:\\Works\\Dictionares\\" + str(len(word)) + ".txt"
        f = open(path, 'r', encoding="UTF-8")
        dictionary = f.readlines()
        f.close()
        result = []
        word = word
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
        f = open("C:\\Works\\log\\nearestWord.txt", 'w', encoding="UTF-8")
        if (len(result2) > 0):
            f.write(result2[0] + " ")
        if (len(result2) > 1):
            f.write(result2[1] + " ")
        if (len(result2) > 2):
            f.write(result2[2] + " ")
        return result2
f = open("C:\\Works\\log\\log.txt", 'r', encoding="UTF-8")
text = f.readlines()
f.close()

for line in text:
    if ("SpellCheck" in line):
        text[text.index(line)] = "SpellCheck start \n"
        break;
    elif (text.index(line) == len(text)-1):
        text.append("SpellCheck start")
if (len(text) == 0):
    text.append("SpellCheck start")
f = open("C:\\Works\\log\\log.txt", 'w', encoding="UTF-8")
f.writelines(text)
f.close()

WordWork.FindSame()

f = open("C:\\Works\\log\\log.txt", 'r', encoding="UTF-8")
text = f.readlines()
f.close()

for line in text:
    if ("SpellCheck" in line):
        text[text.index(line)] = "SpellCheck start end \n"
        break;
f = open("C:\\Works\\log\\log.txt", 'w', encoding="UTF-8")
f.writelines(text)
f.close()
