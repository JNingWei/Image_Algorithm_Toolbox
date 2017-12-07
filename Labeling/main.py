# coding=utf-8

"""
Labeling_Tool
Visiable tool for labeling bbox.

Written by JNing Wei
"""

from __future__ import division
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import glob

# colors for the bboxes
COLORS = ['green', 'cyan', 'blue', 'purple', 'red', 'orange', 'yellow', 'brown', 'pink', 'magenta']
# image sizes for the examples
SIZE = 500, 500

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("207LabelTool")
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.parent.resizable(width = tk.FALSE, height = tk.FALSE)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------

        # dir entry & load
        self.label = tk.Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = tk.E)
        self.entry = tk.Entry(self.frame)
        self.entry.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        self.ldBtn = tk.Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        # main panel for labeling
        self.mainPanel = tk.Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.leftClick)
        self.mainPanel.bind("<Button-3>", self.rightClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column = 1, rowspan = 4, sticky = tk.W+tk.N)
        # showing bbox info & delete bbox
        self.lb1 = tk.Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 1, column = 2, sticky = tk.W)
        self.listbox = tk.Listbox(self.frame, width = 24, height = 60)
        self.listbox.grid(row = 2, column = 2, sticky = tk.N)
        self.btnDel = tk.Button(self.frame, text = 'Delete', command = self.delBBox)
        self.btnDel.grid(row = 3, column = 2, sticky = tk.W+tk.E+tk.N)
        self.btnClear = tk.Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 4, column = 2, sticky = tk.W+tk.E+tk.N)
        # control panel for image navigation
        self.ctrPanel = tk.Frame(self.frame)
        self.ctrPanel.grid(row = 5, column = 1, columnspan = 2, sticky = tk.W+tk.E)
        self.prevBtn = tk.Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = tk.LEFT, padx = 5, pady = 3)
        self.nextBtn = tk.Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = tk.LEFT, padx = 5, pady = 3)
        self.progLabel = tk.Label(self.ctrPanel, text = "")
        self.progLabel.pack(side = tk.LEFT, padx = 5)
        self.tmpLabel = tk.Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = tk.LEFT, padx = 5)
        self.idxEntry = tk.Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = tk.LEFT)
        self.goBtn = tk.Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = tk.LEFT)
        self.egPanel = tk.Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = tk.N+tk.E)
        self.tmpLabel2 = tk.Label(self.egPanel, text = "Pic:")
        self.tmpLabel2.pack(side = tk.TOP, pady = 5)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(tk.Label(self.egPanel))
            self.egLabels[-1].pack(side = tk.TOP)
        self.disp = tk.Label(self.ctrPanel, text='')
        self.disp.pack(side = tk.RIGHT)
        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)
        self.center_window()
        self.menu()

    def menu(self):
        menubar = tk.Menu(self.parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=filemenu)
        filemenu.add_command(label='<Esc>     cancel')
        filemenu.add_command(label='<A>       prev')
        filemenu.add_command(label='<D>       next')
        self.parent.config(menu=menubar)

    def center_window(self):
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        w = 1050
        h = 900
        # w = 750
        # h = 600
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # 加载目录
    def loadDir(self):
        s = self.entry.get()
        self.category = int(s)
        self.imageDir = os.path.join('./Images', str(self.category))
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        self.imageList = sorted(self.imageList)
        if len(self.imageList) == 0:
            print('No .jpg images found in the specified dir!')
            return
        self.cur = 1
        self.total = len(self.imageList)
        self.outDir = os.path.join('./Labels', str(self.category))
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
        self.loadImage()
        print('%d images loaded from %s' %(self.total, s))

    def refreshBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def loadImage(self):
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=tk.NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))
        self.refreshBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        continue
                    tmp = [int(t) for t in line.split()]
                    self.bboxList.append(tuple(tmp))
                    tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1],
                                                            tmp[2], tmp[3],
                                                            width = 3,
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(tk.E, '({:>3d}, {:>3d}) -> ({:>3d}, {:>3d})'.format(tmp[0], tmp[1], tmp[2], tmp[3]))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            self.bboxList.sort()
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print('Image No. %d saved' %(self.cur))

    def leftClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            self.bboxList.append((x1, y1, x2, y2))
            self.bboxIdList.append(self.bboxId)
            self.bboxIdList.sort()
            self.bboxId = None
            self.listbox.insert(tk.END, '(%d, %d) -> (%d, %d)' %(x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'],
                                                          event.x, event.y,
                                                          width = 3,
                                                          outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        if tk.messagebox.askyesno(title='Warning', message='Are you sure to clear all ?'):
            for idx in range(len(self.bboxIdList)):
                self.mainPanel.delete(self.bboxIdList[idx])
            self.listbox.delete(0, len(self.bboxList))
            self.bboxIdList = []
            self.bboxList = []

    def rightClick(self, event):
        if 1 == self.STATE['click']:
            self.cancelBBox(event)
        else:
            self.ask_delete(event)

    def ask_delete(self, event):
        if tk.messagebox.askyesno(title='', message='Delete it ?'):
            corresponding_idx = 1000
            for idx, bbox in enumerate(self.bboxList):
                x1, y1, x2, y2 = bbox
                if event.x > x1 and event.x < x2 and event.y > y1 and event.y < y2 :
                    corresponding_idx = idx
            if corresponding_idx != 1000:
                self.mainPanel.delete(self.bboxIdList[corresponding_idx])
                self.bboxIdList.pop(corresponding_idx)
                self.bboxList.pop(corresponding_idx)
                self.listbox.delete(corresponding_idx)

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

if __name__ == '__main__':
    root = tk.Tk()
    tool = LabelTool(root)
    root.mainloop()
