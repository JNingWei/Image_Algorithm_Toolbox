# Image_Algorithm_Toolbox　 ![Language](https://img.shields.io/badge/language-Python3-orange.svg) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md) ![AD](https://img.shields.io/badge/东半球最好的-图像标记工具-ff69b4.svg)


-----------------


| **`Linux CPU`** | **`Linux GPU`** | **`Mac OS CPU`** | **`Windows CPU`** | **`Windows GPU`** | 
|-----------------|---------------------|------------------|-------------------|---------------|
| ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) |


**Update 23-10-2017: It's an image algorithm toolbox.**

MIT license. Contributions welcome.

## Introduction

    Image_Algorithm_Toolbox/      root dir  根目录
	     |
	     |
	     +-- Enhancing_Tool/      data enhancing tool  图片数据增强工具
	     |         |
	     |         +-- sync_enhancing.py       main program  主程序
	     |         |
	     |         +-- src/         	   pics to be enhanced (need build by yourself)  存放待增强的数据集(需自己新建)
	     |         |
	     |         +-- dst/                    pics be enhanced (automatically build by program)  存放已增强的数据集(程序自动新建)
	     |
	     |
	     +-- Formatting_Tool/     format conversion tool  格式转换工具
	     |         |
	     |         +-- format_conversion.py    main program  主程序
	     |         |
	     |         +-- src/         	   pics to be formatted (need build by yourself)  存放待格式转换的文件(需自己新建)
	     |         |
	     |         +-- dst/                    pics be formatted (automatically build by program)  存放同名的已转换文件(程序自动新建)
	     |
	     |
	     +-- Labeling_Tool/       labeling tool  图片标记工具
	     |         |
	     |         +-- labeling.py             main program  主程序
	     |         |
	     |         +-- src/         	   pics to be marked (need build by yourself)  存放待标注的图片(需自己新建)
	     |         |
	     |         +-- dst/                    pics be marked (automatically build by program)  存放同名的已标注文件(程序自动新建)
	     |
	     |
	     +-- Resizing_Tool/       resizing tool  图片缩放工具
	     |         |
	     |         +-- pic_resizing.py         main program 1  主程序1(只缩放图片)
	     |         |
	     |         +-- sync_resizing.py        main program 2  主程序2(同步缩放图片和标记文件)
	     |         |
	     |         +-- src/         	   pics to be marked (need build by yourself)  存放待缩放的数据集(需自己新建)
	     |         |
	     |         +-- dst/                    pics be marked (automatically build by program)  存放同名的已缩放(程序自动新建)	    数据集 
	     |
	     |
	     +-- README.md            manual of project  说明手册
	     |
	     |
	     +-- LICENSE.md           license of project  许可证
	     |
	     |
	     +-- requirements.txt     environment required for this program  环境要求

## Usage

### data enhancing tool  图片数据增强工具

1. ```cd Enhancing_Tool/```
2. Build *src/* dir
3. Copy 
2. 将待缩放图片拷至 *Origin* 文件夹下；
3. 执行指令　```python main.py```，完成批量图片缩放；
4. 缩放后的图片自动保存在 *Resized* 文件夹下。

### format conversion tool  格式转换工具

1. ```cd ./Resizing```
2. 将待缩放图片拷至 *Origin* 文件夹下；
3. 执行指令　```python main.py```，完成批量图片缩放；
4. 缩放后的图片自动保存在 *Resized* 文件夹下。

### labeling tool  图片标记工具

1. ```cd ./Resizing```
2. 将待缩放图片拷至 *Origin* 文件夹下；
3. 执行指令　```python main.py```，完成批量图片缩放；
4. 缩放后的图片自动保存在 *Resized* 文件夹下。

### resizing tool  图片缩放工具

1. ```cd ./Labeling```
2. 将待标注图片拷至 *Images* 文件夹下；
3. 执行指令　```python main.py```，打开工具窗口；
4. 开始标注（具体见 **Demo**）；
5. 已标注图片会在 *Labels* 文件夹下生成同名文件。

## Demo
Open the labeling tool:
![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/0.png)

<br>

Input the name of sub folder:
![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/2.png)

<br>

Automatically load corresponding Image:
![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/3.png)

<br>

Automatically create document of the same name:
![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/5.png)

<br>

Specify the coordinates use single left-click, every two clicks to determine a diagonal box. Right click cancel.:
![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/4.png)

<br>

Automatically create messages of marked boxes:

![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/6.png)

<br>

Please enjoy the labeling process (≧▽≦)y :
![](https://github.com/parnec/Labeling_Tool/blob/master/.demo/7.png)
<br>


## Requirements

1. Python3.x
2. OpenCV3.x

## Possible problems

May meet ```AttributeError``` by python2.

1. Replace the head lines:
```python
import tkinter as tk
import tkinter.messagebox
```
&emsp;with:
```python
import Tkinter as tk
from Tkinter import *
import tkMessageBox
```

2. Replace ```tk.messagebox.askyesno```(appear twice in line 241、255) with ```tkMessageBox.askyesno```.

Then error will be fixed.

## License

[MIT](https://github.com/parnec/Labeling_tool/blob/master/LICENSE.md)

