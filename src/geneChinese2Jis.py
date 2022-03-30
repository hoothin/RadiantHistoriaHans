import csv
import os

'''
根据光辉物语翻译文本统计汉字并生成码表
author:hoothin
'''

inputPath = ".\\langTransTest.csv"
zhWordsPath = ".\\zhWords.txt"
zhCountPath = ".\\zhCount.txt"
baseJaWordsPath = ".\\baseJaWords.txt"
charsetTargetPath = ".\\charset.txt"
charsetFakePath = ".\\charsetFake.txt"

# 汉字从亜\x88\x9f开始，因此从亜开始，同时复用88以下的假名字母以及符号
# 第一位字节 使用0x81-0x9F、0xE0-0xEF (共47个)
# 第二位字节 使用0x40-0x7E、0x80-0xFC (共188个)
highByte = 0x88
lowByte = 0x9f

zhCount = {}
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
        print(highByte)
        print(lowByte)
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

def checkWords(words):
    global zhCount
    global zhWords
    global jaStr
    result = ""
    for word in words:
        if word not in zhWords:
            if word in jaStr:
                continue
            else:
                zhWords[word] = getCode()
        if word not in zhCount:
            zhCount[word] = 0
        zhCount[word] = zhCount[word] + 1

def main():
    global zhCount
    global zhWords
    global jaStr
    print("Reading translation file...")
    initLang()
    charsetTarget = jaStr + "\n"
    charsetFake = charsetTarget
    index = 0
    with open(inputPath, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            checkWords(row[2])
    with open(zhWordsPath, 'w+', encoding = 'utf-8') as zhWordsFile:
        for i in zhWords:
            zhWordsFile.write(str(i) + " " + zhWords[i] + "\n")
            charsetTarget += i
            charsetFake += zhWords[i]
            index += 1
            if index % 16 == 0:
                charsetTarget += "\n"
                charsetFake += "\n"
    with open(zhCountPath, 'w+', encoding = 'utf-8') as zhCountFile:
        for i in zhCount:
            zhCountFile.write(str(i) + " " + str(zhCount[i]) + "\n")
    with open(charsetTargetPath, 'w+', encoding = 'utf-16') as charsetTargetFile:
        charsetTargetFile.write(charsetTarget)
        charsetTargetFile.close()
    with open(charsetFakePath, 'w+', encoding = 'utf-16') as charsetFakeFile:
        charsetFakeFile.write(charsetFake)
        charsetFakeFile.close()
    print("Generate zhWordsFile over")
    return

if __name__ == '__main__':
    main()