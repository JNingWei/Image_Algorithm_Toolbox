# coding=utf-8

"""
Image_Algorithm_Toolbox
Resize pic to defined size.

__author__ = 'JNingWei'
"""

src = './src'    # dir for origin pics
dst = './dst'    # dir for resized pics
new_size = (1024, 1024)   # new size

import os
origin_pics = [os.path.join(src, name) for name in os.listdir(src) if name.endswith('jpg') or name.endswith('JPG')
               or name.endswith('png') or name.endswith('PNG')]

origin_pics.sort()


# remove dst dir every time
import shutil
try:
    shutil.rmtree(dst)
except OSError:
    pass
os.makedirs(dst)

# main operation
import cv2
# for i, origin_pic in enumerate(origin_pics):
#     img = cv2.imread(origin_pic)
#     resized_pic = cv2.resize(img, new_size)
#     cv2.imwrite('{}/{:>03d}.jpg'.format(dst, i+1), resized_pic)
for origin_pic in origin_pics:
    img = cv2.imread(origin_pic)
    resized_pic = cv2.resize(img, new_size)
    cv2.imwrite(origin_pic.replace(src, dst), resized_pic)
