import csv
import os

'''
导出光辉物语日文与英文文本
author:hoothin
'''
output = ".\\lang.csv"
ext = "msg"

def getMsgList():
    for root, ds, fs in os.walk(".\\ja"):
        for f in fs:
            if f.endswith('.' + ext):
                fullname = os.path.join(root, f)
                yield fullname

def main():
    with open(output, 'a+', encoding = 'utf-8', newline='') as csvfile:
        print("Getting japanese")
        writer = csv.writer(csvfile)
        for msgFile in getMsgList():
            fp = open(msgFile, encoding = 'shift-jis')
            jaStr = fp.read()
            print("Writing {} to csv".format(msgFile))
            fp = open(msgFile.replace("\\ja\\","\\en\\"), encoding = 'shift-jis')
            enStr = fp.read()
            writer.writerow([jaStr, enStr, msgFile])
        csvfile.close()
    return

if __name__ == '__main__':
    main()