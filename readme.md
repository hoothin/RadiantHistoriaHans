# 3DS光辉物语汉化笔记
招募日翻英翻
照目前的人手和进度，估计没个十年出不来了
![img](main.jpg)


# Table of Contents

1.  [解密](#org63728f7)
2.  [解包](#orgc9603c9)
3.  [定位](#org0bd59af)
    1.  [对话文本](#org389afaf)
    2.  [系统文本](#org9261a97)
    3.  [图片](#org405807a)
    4.  [YesOrNo](#org5a30068)
4.  [制作字库](#orgf42d281)
    1.  [根据bcfnt导出](#orgb398672)
        1.  [导出字符列表](#org7923b50)
        2.  [导出字符排序](#org942f1bc)
    2.  [导出](#org8fe0c90)
        1.  [根据xllt xlor导出](#org81f7009)
        2.  [修改导出](#orgb155329)
    3.  [shiftjis映射](#orgf873c8a)
        1.  [获取所有日文汉字，保存为shiftjis编码](#orge55dc63)
        2.  [对日文汉字进行排序，将所有可复用的字符提前](#orgb8da683)
        3.  [将所有可复用的字符保存为unicode编码](#org1b629df)
        4.  [从末尾开始新增汉字](#org5c4b46c)
        5.  [用新增汉字替换对应位置的日文汉字，生成图片、伪装字体以及映射至shiftjis编码的码表](#org878498e)
5.  [自动化](#orgd0316cb)
    1.  [根据bcfnt导出](#org2aad38b)
    2.  [生成xllt文件](#orgcaa3946)
    3.  [提取英日文本并生成csv，然后机翻](#orge48a43d)
    4.  [根据翻译后csv导入文本](#orge75ab11)
    5.  [根据零碎文本生成伪装shift-jis代码](#orgde00049)



<a id="org63728f7"></a>

# 解密

使用3ds\_decrypt\_v2


<a id="orgc9603c9"></a>

# 解包

使用DotNet3dsToolkit146


<a id="org0bd59af"></a>

# 定位


<a id="org389afaf"></a>

## 对话文本

根据名称分析可知位于Message文件夹


<a id="org9261a97"></a>

## 系统文本

解包美版rom，将所有文件复制进Citra日版游戏的Mod位置，再挨个移除，确定系统文本位于Table，通过UltraEdit在目录（Table文件夹）中搜索-高级-使用编码-shift-JIS（通过对话文本编码可知），搜索游戏中出现的系统文本，可定位至文件


<a id="org405807a"></a>

## 图片

同上，可知位于Texture文件夹，编辑stex文件即可修改


<a id="org5a30068"></a>

## YesOrNo

这些字符居然被硬编码在可执行文件里了，还好知道它用的是shift-jis编码。通过（Yes=8278 8285 8293）(No=826d 828f)（はい=82CD 82A2）（いいえ=82a2 82a2 82a6）定位，更改为“确定取消”的伪装编码。总共有5处


<a id="orgf42d281"></a>

# 制作字库


<a id="orgb398672"></a>

## 根据bcfnt导出

导出txt

    3dsfont\bcfnt2charset CHIARO_14.bcfnt CHIARO_14.txt

txt文档包含信息有：字符列表与字符排列顺序


<a id="org7923b50"></a>

### 导出字符列表

    3dsfont\charset2xllt CHIARO_14.txt CHIARO_14.xllt


<a id="org942f1bc"></a>

### 导出字符排序

    3dsfont\charset2xlor CHIARO_14.txt CHIARO_14.xlor


<a id="org8fe0c90"></a>

## 导出目标字库


<a id="org81f7009"></a>

### 根据xllt xlor导出


<a id="orgb155329"></a>

### 修改导出

1.  修改xllt中的unicode代码可增删字符，增添字符需要指定系统字体

2.  修改xlor中的unicode代码可在导出图片时变更字符的排序


<a id="orgf873c8a"></a>

## shiftjis映射


<a id="orge55dc63"></a>

### 获取所有日文汉字


<a id="orgb8da683"></a>

### 对日文汉字进行排序，将所有可复用的字符提出


<a id="org1b629df"></a>

### 将所有可复用的字符保存为unicode编码


<a id="org5c4b46c"></a>

### 从末尾开始新增汉字


<a id="org878498e"></a>

### 用新增汉字替换对应位置的日文汉字，生成图片、伪装字体以及映射至shiftjis编码的码表


<a id="orgd0316cb"></a>

# 自动化
详见代码

<a id="org2aad38b"></a>

## 根据bcfnt导出

将3dsfont与FontConverter置于同一文件夹下，将bcfnt拷贝至此文件夹

    @set str=%~nx1
    @set a=%str:~0,-6%
    3dsfont\bcfnt2charset %a%.bcfnt %a%.txt
    3dsfont\charset2xlor %a%.txt FontConverter\xlor\%a%.xlor
    3dsfont\charset2xllt %a%.txt FontConverter\xllt\%a%.xllt
    Pause

新建bat文件，将bcfnt拖至此bat上
需注意3dsfont只能生成utf16编码的文件


<a id="orgcaa3946"></a>

## 生成xllt文件

geneChinese2Jis.py
统计出现的所有字符并拼接基本文本（假名英文字母符号）生成伪装码表与真实码表
根据真实码表生成字体bmp，根据伪装码表生成xllt与xlor
最后结合以上三者生成bcfnt


<a id="orge48a43d"></a>

## 提取英日文本并生成csv，然后机翻

exportLang.py
translateByGoogle.py
translateByPygtrans.py


<a id="orge75ab11"></a>

## 根据翻译后csv导入文本

importLang.py


<a id="orgde00049"></a>

## 根据零碎文本生成伪装shift-jis代码

convertZh2Jis.py

