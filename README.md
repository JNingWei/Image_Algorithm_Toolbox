# Wood_Tool

**Update 23-10-2017: It's a toolbox contains labeling tool and resizing tool.**

## Introduction

	Wood_Tool        根目录
	     |
	     |
	     +-- README.html      说明文档
	     |
	     |
	     +-- Labeling         图片标注工具
	     |    |
	     |    +-- main.py         主程序
	     |    |
	     |    +-- Images          存放待标注图片
	     |    |
	     |    +-- Labels          存放已标注同名文件
	     |
	     |
	     +-- Resizing         图片缩放工具
		  |
		  +-- main.py         主程序
		  |
		  +-- Origin          存放待缩放图片
		  |
		  +-- Resized         存放已缩放图片


## Usage

### 图片标注工具

1. cd ./Labeling
2. 将待标注图片拷至 Images 文件夹下；
3. 执行指令　python main.py，打开工具窗口；
4. 开始标注；
5. 已标注图片会在 Labels 文件夹下生成同名文件。

### 图片缩放工具

1. cd ./Resizing
2. 将待缩放图片拷至 Origin 文件夹下；
3. 执行指令　python main.py，完成批量图片缩放；
4. 缩放后的图片自动保存在 Resized 文件夹下。

## Requirements

1. Python2.x
2. OpenCV3.x

## License

[MIT]()

