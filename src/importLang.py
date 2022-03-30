import csv
import os

'''
根据光辉物语翻译文本与码表生成源文件
author:hoothin
'''

inputFile = ".\\langTransTest.csv"
savePath = ".\\Message"
zhWordsPath = ".\\zhWords.txt"

def initLang():
    global zhWords
    zhWords = {}
    with open(zhWordsPath, 'r', encoding = 'utf-8') as zhWordsFile:
        zhStrs = zhWordsFile.readlines()
        for zhStr in zhStrs:
            zhStrDict = zhStr.strip().split(" ")
            zhWords[zhStrDict[0]] = zhStrDict[1]
    return

def getWordsCode(words):
    global zhWords
    result = ""
    for word in words:
        if word in zhWords:
            result += zhWords[word]
        else:
            result += word
    return result

def main():
    global zhCount
    print("Importing...")
    initLang()
    with open(inputFile, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            filePath = savePath + row[3].replace(".\\ja", "")
            fileDir = os.path.dirname(filePath)
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            with open(filePath, 'w+', encoding = 'cp932') as msgfile:
                msgfile.write(getWordsCode(row[2]))
                msgfile.close()
    print("Import over")
    return

if __name__ == '__main__':
    main()