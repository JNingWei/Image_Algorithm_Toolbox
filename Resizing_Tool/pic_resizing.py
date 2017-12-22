# coding=utf-8

"""
Image_Algorithm_Toolbox
Resize pic to defined size.

__author__ = 'JNingWei'
"""


import os
import cv2


def dst_check(dst):
    import shutil
    try:
        shutil.rmtree(dst)
    except OSError:
        pass
    os.makedirs(dst)


def get_path_lists(src):
    check_suffix = lambda x : True if os.path.splitext(x)[1] in [".jpg", ".JPG", ".png", ".PNG"] else False
    src_image_paths = [os.path.join(src, name) for name in os.listdir(src) if check_suffix(name)]
    assert len(src_image_paths)
    src_image_paths.sort()
    dst_image_paths = [path.replace("src", "dst").replace(os.path.splitext(path)[1], os.path.splitext(path)[1].lower()) for path in src_image_paths]
    return src_image_paths, dst_image_paths

def resize_image(src_image_path, dst_image_path, origin_size, new_size, idx):
    src_image = cv2.imread(src_image_path)
    dst_image = cv2.resize(src_image, new_size)
    cv2.imwrite(dst_image_path, dst_image)


def main(src, dst, new_size):
    dst_check(dst)
    idx = 0
    src_image_paths, dst_image_paths = get_path_lists(src)
    for (src_image_path, dst_image_path) in zip(src_image_paths, dst_image_paths):
        resize_image(src_image_path, dst_image_path, None, new_size, idx)
        idx += 1


if __name__ == "__main__":
    SRC = './src'    # dir for origin pics
    DST = './dst'    # dir for resized pics
    NEW_SIZE = (800, 800)   # new size
    main(SRC, DST, NEW_SIZE)
