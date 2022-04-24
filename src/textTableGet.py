import csv
import os

'''
获取光辉物语杂项日文与英文文本
author:hoothin
'''
tableDir = ".\\textTable"
output = ".\\textTable.csv"

# 0000|ffff 81~ef 不是00 00 2个一跳 检查并存储指针位置与文本长度
table1 = [
    "MapTable.bin",
    "CharaName.dat",
    "CreditDataTable.dat",
    "GlossaryTable.dat",
    "WorldMapTable.dat"
]
#4开始，間隔 a4 標題描述间隔20
table2 = [
    "AccessoryNameTable.dat",
    "ArmorNameTable.dat",
    "ItemNameTable.dat",
    "WeaponNameTable.dat"
]
#30开始存储开始指针，00分隔
table3 = {
    "BattleConditionIconTable.dat":0x269,
    "ChronicleEventTitle.dat":0x1094,
    "ChronicleStory.dat":0x171c,
    "ChronicleSubTitle.dat":0x1e4,
    "ChronicleTitle.dat":0x1e4,
    "DLCTextTable.bin":0x318,
    "EventCharaTable.dat":0x2048,
    "EventCommonMessageTable.dat":0x110,
    "EventProcessTable.dat":0x1b20,
    "EventTitleTable.dat":0x2e0,
    "HelpMsgTable.dat":0x3fb,
    "QuestTable.dat":0x72c,
    "SaveLoadTextTable.dat":0x285,
    "SelectComdTable.dat":0x514,
    "SelectTextTable.dat":0xf5,
    "TitleTextTable.dat":0x23d
}
fileIndex = 0
def getType1():
    global fileIndex
    for file in table1:
        fullname = tableDir + "\\ja\\" + file
        fullnameEn = tableDir + "\\en\\" + file
        print("Reading ",file)
        checkArr = []
        curPointer = 0
        curTextBytes = b""
        index = 0
        findEnd = False
        with open(output, 'a+', encoding = 'utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            with open(fullname, "rb") as fp:
                with open(fullnameEn, "rb") as fpEn:
                    curByte = fp.read(1)
                    while curByte:
                        checkArr.append(int.from_bytes(curByte, byteorder='big'))
                        if len(checkArr) == 5:
                            checkArr.pop(0)
                        if curTextBytes != b"":
                            if int.from_bytes(curByte, byteorder='big') == 0x00:
                                findEnd = True
                            else:
                                if findEnd:
                                    try:
                                        fpEn.seek(curPointer + 1);
                                        enBytes = fpEn.read(index - curPointer - 1)
                                        enStr = enBytes.decode('shift-jis').strip(b'\x00'.decode())
                                        jaStr = curTextBytes.decode('shift-jis')
                                        if jaStr != enStr:
                                            writer.writerow([jaStr, enStr, (index - curPointer - 1) / 2, curPointer, fileIndex])
                                    except Exception as e:
                                        pass
                                    curTextBytes = b""
                                else:
                                    curTextBytes = curTextBytes + curByte
                        else:
                            if len(checkArr) < 4:
                                pass
                            elif ((checkArr[0] == 0x00 and checkArr[1] == 0x00) or (checkArr[0] == 0xFF and checkArr[1] == 0xFF)) and checkArr[2] >= 0x81 and checkArr[2] <= 0xEF and checkArr[3] != 0x00:
                                curTextBytes = checkArr[2].to_bytes(1, byteorder='big') + checkArr[3].to_bytes(1, byteorder='big')
                                curPointer = index - 2
                                findEnd = False
                        curByte = fp.read(1)
                        index += 1
                    if curTextBytes != b"":
                        try:
                            fpEn.seek(curPointer + 1);
                            enBytes = fpEn.read(index - curPointer - 1)
                            enStr = enBytes.decode('shift-jis').strip(b'\x00'.decode())
                            jaStr = curTextBytes.decode('shift-jis')
                            if jaStr != enStr:
                                writer.writerow([jaStr, enStr, (index - curPointer - 1) / 2, curPointer, fileIndex])
                        except Exception as e:
                            pass
        fileIndex += 1

def getType2():
    global fileIndex
    for file in table2:
        fullname = tableDir + "\\ja\\" + file
        fullnameEn = tableDir + "\\en\\" + file
        print("Reading ",file)
        index = 4
        with open(output, 'a+', encoding = 'utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            with open(fullname, "rb") as fp:
                with open(fullnameEn, "rb") as fpEn:
                    curByte = fp.read(index)
                    while curByte:
                        try:
                            curByte = fp.read(0x20)
                            fpEn.seek(index);
                            enBytes = fpEn.read(0x20)
                            enStr = enBytes.decode('shift-jis').strip(b'\x00'.decode())
                            jaStr = curByte.decode('shift-jis').strip(b'\x00'.decode())
                            if jaStr != enStr:
                                writer.writerow([jaStr, enStr, 0x10, index, fileIndex])
                            curByte = fp.read(0x80)
                            enBytes = fpEn.read(0x80)
                            enStr = enBytes.decode('shift-jis').strip(b'\x00'.decode())
                            jaStr = curByte.decode('shift-jis').strip(b'\x00'.decode())
                            if jaStr != enStr:
                                writer.writerow([jaStr, enStr, 0x40, index + 0x20, fileIndex])
                        except Exception as e:
                            pass
                        curByte = fp.read(0x4)
                        index += 0xa4
        fileIndex += 1

def getType3():
    global fileIndex
    for file in table3:
        fullname = tableDir + "\\ja\\" + file
        fullnameEn = tableDir + "\\en\\" + file
        jaStrArr = []
        enStrArr = []
        pointer = table3[file]
        print("Reading ",file)
        curTextBytes = b""
        with open(output, 'a+', encoding = 'utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            with open(fullname, "rb") as fp:
                index = pointer
                fp.seek(pointer)
                curPointer = pointer
                curByte = fp.read(1)
                while curByte:
                    if int.from_bytes(curByte, byteorder='big') == 0x00:
                        if curTextBytes != b"":
                            try:
                                jaStr = curTextBytes.decode('shift-jis')
                                jaStrArr.append([jaStr, (index - curPointer) / 2, curPointer, fileIndex])
                                curPointer = index + 1
                                curTextBytes = b""
                            except Exception as e:
                                pass
                    else:
                        curTextBytes = curTextBytes + curByte
                    curByte = fp.read(1)
                    index += 1
                if curTextBytes != b"":
                    try:
                        jaStr = curTextBytes.decode('shift-jis')
                        jaStrArr.append([jaStr, (index - curPointer) / 2, curPointer, fileIndex])
                    except Exception as e:
                        pass
            with open(fullnameEn, "rb") as fpEn:
                curTextBytes = b""
                index = pointer
                fpEn.seek(pointer)
                curPointer = pointer
                curByte = fpEn.read(1)
                while curByte:
                    if int.from_bytes(curByte, byteorder='big') == 0x00:
                        if curTextBytes != b"":
                            try:
                                enStr = curTextBytes.decode('shift-jis')
                                enStrArr.append(enStr)
                                curPointer = index
                                curTextBytes = b""
                            except Exception as e:
                                pass
                    else:
                        curTextBytes = curTextBytes + curByte
                    curByte = fpEn.read(1)
                    index += 1
                if curTextBytes != b"":
                    try:
                        enStr = curTextBytes.decode('shift-jis')
                        enStrArr.append(enStr)
                        curPointer = index
                        curTextBytes = b""
                    except Exception as e:
                        pass
            for x in range(len(jaStrArr)):
                if x >= len(enStrArr):
                    jaStrArr[x].insert(1, "")
                else:
                    jaStrArr[x].insert(1, enStrArr[x])
                writer.writerow(jaStrArr[x])
        fileIndex += 1

if __name__ == '__main__':
    getType1()
    getType2()
    getType3()