from pygtrans import Translate
import csv
import time
import re

'''
使用pygtrans机翻并写入csv
author:hoothin
'''
# inputFile = "./lang.csv"
# outputFile = "./langTrans1.csv"
inputFile = "./textTable.csv"
outputFile = "./textTableTrans.csv"

#如果中断了更改此值接续
startPos = 0;
def main():
    data = []
    transBody = []
    print("Reading input file")
    client = Translate()
    with open(inputFile,'r',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            transBody.append(row[0])
            transBody.append(row[1])
            data.append(row)

    print("Translating")
    transResult = client.translate(transBody)
    print("Translate over")
    for i in range(len(data)):
        jaTrans=transResult[i * 2].translatedText[0]
        enTrans=transResult[i * 2 + 1].translatedText[0]
        data[i][0] = data[i][0] + "\n" + jaTrans
        data[i][1] = data[i][1] + "\n" + enTrans 
        data[i].insert(2,jaTrans)
    with open(outputFile, "w", encoding = "utf-8", newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return

if __name__ == '__main__':
    main()