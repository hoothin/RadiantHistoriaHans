from googletrans import Translator
import csv
import time
import re

'''
使用谷歌机翻并写入csv
author:hoothin
'''
inputFile = "./lang.csv"
outputFile = "./langTrans.csv"

#如果中断了更改此值接续
startPos = 0;
def main():
    data = []
    print("Reading input file")
    translator = Translator()
    runtimes = 0
    with open(inputFile, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        with open(outputFile, "w", encoding = "utf-8", newline = '') as csvfile:
            writer = csv.writer(csvfile)
            for row in reader:
                if runtimes < startPos:
                    continue
                print("Translating {}".format(row[2]))
                try:
                    jaTrans = translator.translate(re.sub(r'\<.*?\>', "", row[0]), dest = "zh-cn").text
                except Exception as e:
                    time.sleep(30)
                    jaTrans = translator.translate(re.sub(r'\<.*?\>', "", row[0]), dest = "zh-cn").text
                try:
                    enTrans = translator.translate(re.sub(r'\<.*?\>', "", row[1]), dest = "zh-cn").text
                except Exception as e:
                    time.sleep(30)
                    enTrans = translator.translate(re.sub(r'\<.*?\>', "", row[1]), dest = "zh-cn").text
                row[0] = row[0] + "\n" + jaTrans
                row[1] = row[1] + "\n" + enTrans
                row.insert(-1, enTrans)
                # data.append(row)
                writer.writerow(row)
                runtimes += 1
                if runtimes % 10 == 0:
                    time.sleep(3)
    return

if __name__ == '__main__':
    main()