import csv
import os

'''
光辉物语码表翻译单个文本并生成shiftjis编码欺骗码
author:hoothin
'''

inputPath = ".\\in.txt"
outputPath = ".\\out.txt"
zhWordsPath = ".\\zhWords.txt"
baseJaWordsPath = ".\\baseJaWords.txt"

highByte = 0x88
lowByte = 0x9f

zhWords = {}
def initLang():
    global zhWords
    global jaStr

    global highByte
    global lowByte
    lastJaWord = ''
    with open(baseJaWordsPath, 'r', encoding = 'utf-8') as jaWordsFile:
        jaStr = jaWordsFile.read()
    with open(zhWordsPath, 'r', encoding = 'utf-8') as zhWordsFile:
        zhStrs = zhWordsFile.readlines()
        for zhStr in zhStrs:
            zhStrDict = zhStr.strip().split(" ")
            zhWords[zhStrDict[0]] = zhStrDict[1]
            lastJaWord = zhStrDict[1]
    if lastJaWord != '':
        wordByte = lastJaWord.encode('shift-jis')
        highByte = int.from_bytes(wordByte, byteorder='little')&0xff
        lowByte = int.from_bytes(wordByte, byteorder='big')&0xff
    return

def getCode():
    global highByte
    global lowByte
    lowByte = lowByte + 1
    if lowByte == 0x7F:
        lowByte = 0x80
    elif lowByte == 0xFD:
        lowByte = 0x40
        highByte = highByte + 1
        if highByte == 0xA0:
            highByte = 0xE0
    return ((highByte<<8)+lowByte).to_bytes(length=2, byteorder='big').decode('shift-jis')

def getWordsCode(words):
    global zhWords
    global jaStr
    result = ""
    for word in words:
        if word not in zhWords:
            if word in jaStr:
                result += word
                continue
            else:
                zhWords[word] = getCode()
        result += zhWords[word]
    return result

def main():
    global zhCount
    print("Converting...")
    initLang()
    inputStr = ''
    with open(inputPath, 'r', encoding = 'utf-8') as inputFile:
        inputStr = inputFile.read()
    with open(outputPath, 'w+', encoding = 'cp932') as outputFile:
        outputFile.write(getWordsCode(inputStr))
        outputFile.close()
    with open(zhWordsPath, 'w+', encoding = 'utf-8') as zhWordsFile:
        for i in zhWords:
            zhWordsFile.write(str(i) + " " + zhWords[i] + "\n")
    print("Convert over")
    return

if __name__ == '__main__':
    main()