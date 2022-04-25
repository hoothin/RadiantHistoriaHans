# 3DS光辉物语汉化笔记
招募日翻英翻 QQ群 20550973

照目前的人手和进度，估计没个十年出不来了
![img](main.jpg)


# Table of Contents

1.  [解密](#org8df8134)
2.  [解包](#orgf81d746)
3.  [定位](#orgfc20e6c)
    1.  [对话文本](#org80ad637)
    2.  [系统文本](#org5fdcb1c)
    3.  [图片](#org41e9909)
    4.  [YesOrNo](#orgd345f24)
4.  [制作字库](#org9740c29)
    1.  [根据bcfnt导出](#org9ab2e9d)
        1.  [导出字符列表](#org606b4bf)
        2.  [导出字符排序](#org29da150)
    2.  [导出](#orgef9d754)
        1.  [根据xllt xlor导出](#org64b51f1)
        2.  [修改导出](#org2275d33)
    3.  [shiftjis映射](#org94b8cd1)
        1.  [获取所有日文汉字，保存为shiftjis编码](#org672d52f)
        2.  [对日文汉字进行排序，将所有可复用的汉字提前](#orga7a7481)
        3.  [将所有可复用的汉字保存为unicode编码](#org7b9075a)
        4.  [从末尾开始新增汉字](#orgb81c0b3)
        5.  [用新增汉字替换对应位置的日文汉字，生成图片、映射字体以及映射至shiftjis编码的码表](#orgcd9a1e5)
5.  [自动化](#orgb9792eb)
    1.  [根据bcfnt导出](#org5401f32)
    2.  [生成xllt文件](#org8ea27a9)
    3.  [提取英日文本并生成csv，然后机翻](#org13e13aa)
    4.  [提取系统文本](#org424d84c)
    5.  [根据翻译后csv导入文本](#org7a4c06f)
    6.  [根据零碎文本生成映射shift-jis代码](#orgd90c020)



<a id="org8df8134"></a>

# 解密

使用3ds\_decrypt\_v2


<a id="orgf81d746"></a>

# 解包

使用DotNet3dsToolkit146


<a id="orgfc20e6c"></a>

# 定位


<a id="org80ad637"></a>

## 对话文本

根据名称分析可知位于Message文件夹


<a id="org5fdcb1c"></a>

## 系统文本

解包美版rom，将所有文件复制进Citra日版游戏的Mod位置，再挨个移除，确定系统文本位于Table，通过UltraEdit在目录（Table文件夹）中搜索-高级-使用编码-shift-JIS（通过对话文本编码可知），搜索游戏中出现的系统文本，可定位至文件。其中有3种格式的文本，分别为：

1.  0000|ffff开头00结尾，2个字节一跳
2.  先用4字节记录序号，再用0x20字节记录标题文本，0x80字节记录描述文本
3.  0x30开始固定位存储开始指针，指向下方文本区域，0x00标记结束符


<a id="org41e9909"></a>

## 图片

同上，可知位于Texture文件夹，编辑stex文件即可修改


<a id="orgd345f24"></a>

## YesOrNo

这些字符居然被硬编码在可执行文件里了，还好知道它用的是shift-jis编码。通过（Yes=8278 8285 8293）(No=826d 828f)（はい=82CD 82A2）（いいえ=82a2 82a2 82a6）定位，更改为确定取消的映射编码。总共有5处


<a id="org9740c29"></a>

# 制作字库


<a id="org9ab2e9d"></a>

## 根据bcfnt导出

导出txt

    3dsfont\bcfnt2charset CHIARO_14.bcfnt CHIARO_14.txt

txt文档包含信息有：字符列表与字符排列顺序


<a id="org606b4bf"></a>

### 导出字符列表

    3dsfont\charset2xllt CHIARO_14.txt CHIARO_14.xllt


<a id="org29da150"></a>

### 导出字符排序

    3dsfont\charset2xlor CHIARO_14.txt CHIARO_14.xlor


<a id="orgef9d754"></a>

## 导出


<a id="org64b51f1"></a>

### 根据xllt xlor导出


<a id="org2275d33"></a>

### 修改导出

1.  修改xllt中的unicode代码可增删字符，增添字符需要指定系统字体

2.  修改xlor中的unicode代码可在导出图片时变更字符的排序


<a id="org94b8cd1"></a>

## shiftjis映射


<a id="org672d52f"></a>

### 获取所有日文汉字，保存为shiftjis编码


<a id="orga7a7481"></a>

### 对日文汉字进行排序，将所有可复用的汉字提前


<a id="org7b9075a"></a>

### 将所有可复用的汉字保存为unicode编码


<a id="orgb81c0b3"></a>

### 从末尾开始新增汉字


<a id="orgcd9a1e5"></a>

### 用新增汉字替换对应位置的日文汉字，生成图片、映射字体以及映射至shiftjis编码的码表


<a id="orgb9792eb"></a>

# 自动化


<a id="org5401f32"></a>

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


<a id="org8ea27a9"></a>

## 生成xllt文件

geneChinese2Jis.py

统计出现的所有字符并拼接基本文本（假名英文字母符号）生成映射码表与真实码表

根据真实码表生成字体bmp，根据映射码表生成xllt与xlor

结合以上三者生成bcfnt


<a id="org13e13aa"></a>

## 提取英日文本并生成csv，然后机翻

exportLang.py

translateByGoogle.py

translateByPygtrans.py


<a id="org424d84c"></a>

## 提取系统文本

textTableGet.py


<a id="org7a4c06f"></a>

## 根据翻译后csv导入文本

importLang.py

textTableImport.py


<a id="orgd90c020"></a>

## 根据零碎文本生成映射shift-jis代码

convertZh2Jis.py

