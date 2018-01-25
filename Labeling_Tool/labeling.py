# coding=utf-8

"""
Image_Algorithm_Toolbox
Visiable tool for labeling bbox.

__author__ = 'JNingWei'
"""

from __future__ import division
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import cv2

# colors for the bboxes
COLORS = ['green', 'cyan', 'blue', 'purple', 'red', 'orange', 'yellow', 'brown', 'pink', 'magenta']

# scaling ratio
SCALING_RATIO = 0

# real_image_size
REAL_IMG_W, REAL_IMG_H = 0, 0

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("Labeling Tool")
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
        self.ldBtn = tk.Button(self.frame, text = "Load", command = self.loadDir, border = 2)
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
        self.listbox = tk.Listbox(self.frame, width = 30, height = 60)
        self.listbox.grid(row = 2, column = 2, sticky = tk.N)
        self.btnDel = tk.Button(self.frame, text = 'Delete', command = self.delBBox, border = 2)
        self.btnDel.grid(row = 3, column = 2, sticky = tk.W+tk.E+tk.N)
        self.btnClear = tk.Button(self.frame, text = 'ClearAll', command = self.clearBBox, border = 2)
        self.btnClear.grid(row = 4, column = 2, sticky = tk.W+tk.E+tk.N)
        # control panel for image navigation
        self.ctrPanel = tk.Frame(self.frame)
        self.ctrPanel.grid(row = 5, column = 1, columnspan = 2, sticky = tk.W+tk.E)
        self.prevBtn = tk.Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage, border = 5)
        self.prevBtn.pack(side = tk.LEFT, padx = 5, pady = 3)
        self.nextBtn = tk.Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage, border = 5)
        self.nextBtn.pack(side = tk.LEFT, padx = 5, pady = 3)
        self.progLabel = tk.Label(self.ctrPanel, text = "")
        self.progLabel.pack(side = tk.LEFT, padx = 5)
        self.tmpLabel = tk.Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = tk.LEFT, padx = 5)
        self.idxEntry = tk.Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = tk.LEFT)
        self.goBtn = tk.Button(self.ctrPanel, text = 'Go', command = self.gotoImage, border = 2)
        self.goBtn.pack(side = tk.LEFT)
        self.exitBtn = tk.Button(self.ctrPanel, text='Exit !', width = 10, command = self.exit, border = 5)
        self.exitBtn.pack(side = tk.RIGHT, padx = 5, pady = 3)
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


    def scaling_panel(self, image_path):
        screen_w, screen_h = self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()
        h, w, _ = cv2.imread(image_path).shape
        aspect_ratio = w / h
        panel_h = int(screen_h - 250)
        panel_w = int(panel_h * aspect_ratio)
        global SCALING_RATIO
        SCALING_RATIO = panel_h / h
        global REAL_IMG_W, REAL_IMG_H
        REAL_IMG_W, REAL_IMG_H = w, h
        if panel_w > screen_w - 150:
            assert "Sorry, the loaded picture is too wide ! Please resize it first."
        return panel_w, panel_h

    def menu(self):
        menubar = tk.Menu(self.parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=filemenu)
        filemenu.add_command(label='<Esc>     cancel')
        filemenu.add_command(label='<A>       prev')
        filemenu.add_command(label='<D>       next')
        self.parent.config(menu=menubar)

    def center_window(self):
        ws, hs = self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()
        w, h = ws - 150, hs - 150
        x = round((ws//2) - (w//2))
        y = round((hs//2) - (h//2))
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # 加载目录
    def loadDir(self):
        self.category = self.entry.get()
        self.imageDir = os.path.join('./src', str(self.category))
        self.imageList = [os.path.join(self.imageDir, pic) for pic in os.listdir(self.imageDir)
                          if os.path.splitext(pic)[1] in [".jpg", ".JPG", ".png", ".PNG"]]
        self.imageList = sorted(self.imageList)
        if len(self.imageList) == 0:
            print('No .jpg images found in the specified dir!')
            return
        self.cur = 1
        self.total = len(self.imageList)
        self.outDir = os.path.join('./dst', str(self.category))
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
        self.loadImage()
        print('%d images loaded from %s' %(self.total, self.category))

    def refreshBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def loadImage(self):
        image_path = self.imageList[self.cur - 1]
        self.img_1 = Image.open(image_path)
        panel_w, panel_h = self.scaling_panel(image_path)
        self.img = self.img_1.resize((panel_w, panel_h),Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = self.tkimg.width(), height = self.tkimg.height())
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=tk.NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))
        self.refreshBBox()
        self.imagename = os.path.split(image_path)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        continue
                    tmp_true = [int(t) for t in line.split()]
                    global SCALING_RATIO
                    scaling = lambda x: int(x * SCALING_RATIO)
                    tmp_scaled = list(map(scaling, tmp_true))
                    self.bboxList.append(tuple(tmp_scaled))
                    tmpId = self.mainPanel.create_rectangle(tmp_scaled[0], tmp_scaled[1],
                                                            tmp_scaled[2], tmp_scaled[3],
                                                            width = 3,
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)

                    self.listbox.insert(tk.E, '({:>3d}, {:>3d}) -> ({:>3d}, {:>3d})'
                                        .format(tmp_true[0], tmp_true[1], tmp_true[2], tmp_true[3]))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('{}\n'.format(len(self.bboxList)))
            self.bboxList.sort()
            global SCALING_RATIO
            recovering = lambda x: int(x / SCALING_RATIO)
            for bbox in self.bboxList:
                bbox = list(map(recovering, bbox))
                bbox = self.check_border(bbox)
                f.write(' '.join(map(str, bbox)) + '\n')
        print('Image No. %d saved' %(self.cur))

    def check_border(self, bbox):
        x1, y1, x2, y2 = bbox
        low_check = lambda k, low_limit: k if k > low_limit else low_limit
        high_check = lambda k, high_limit: k if k < high_limit else high_limit
        global REAL_IMG_W, REAL_IMG_H
        x1 = high_check(low_check(x1, 1), REAL_IMG_W-1)
        y1 = high_check(low_check(y1, 1), REAL_IMG_H-1)
        x2 = high_check(low_check(x2, 1), REAL_IMG_W-1)
        y2 = high_check(low_check(y2, 1), REAL_IMG_H-1)
        return x1, y1, x2, y2

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

            recovering = lambda x: int(x / SCALING_RATIO)
            x1, y1, x2, y2 = list(map(recovering, [x1, y1, x2, y2]))
            x1, y1, x2, y2 = self.check_border([x1, y1, x2, y2])

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

    def exit(self, event = None):
        self.saveImage()
        exit(0)


if __name__ == '__main__':
    root = tk.Tk()
    tool = LabelTool(root)
    root.mainloop()

