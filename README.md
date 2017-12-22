# Image_Algorithm_Toolbox　 ![Language](https://img.shields.io/badge/language-Python3-orange.svg) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md) ![AD](https://img.shields.io/badge/东半球最好的-图像标记工具-ff69b4.svg)


-----------------


| **`Linux CPU`** | **`Linux GPU`** | **`Mac OS CPU`** | **`Windows CPU`** | **`Windows GPU`** | 
|-----------------|---------------------|------------------|-------------------|---------------|
| ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) | ![Travis](https://img.shields.io/travis/rust-lang/rust/master.svg) |


**Update 23-10-2017: It's an image algorithm toolbox.**

MIT license. Contributions welcome.

## Introduction

	Labeling_Tool        根目录
	     |
	     |
	     +-- README.html      说明文档
	     |
	     |
	     +-- Labeling         图片标注工具
	     |    |
	     |    +-- main.py         主程序
	     |    |
	     |    +-- Images/         存放待标注图片(需自己新建)
	     |    |
	     |    +-- Labels/         存放已标注同名文件(程序自动新建)
	     |
	     |
	     +-- Resizing         图片缩放工具
		  |
		  +-- main.py         主程序
		  |
		  +-- Origin/         存放待缩放图片(需自己新建)
		  |
		  +-- Resized/        存放已缩放图片(程序自动新建)


## Usage

### 图片缩放工具

1. ```cd ./Resizing```
2. 将待缩放图片拷至 *Origin* 文件夹下；
3. 执行指令　```python main.py```，完成批量图片缩放；
4. 缩放后的图片自动保存在 *Resized* 文件夹下。

### 图片标注工具

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

Replace the head lines:
```python
import tkinter as tk
import tkinter.messagebox
```

with:
```python
import Tkinter as tk
from Tkinter import *
import tkMessageBox
```

And replace ```tk.messagebox.askyesno```(appear twice in line 241、255) with ```tkMessageBox.askyesno```.

Then error will be fixed.

## License

[MIT](https://github.com/parnec/Labeling_tool/blob/master/LICENSE.md)

