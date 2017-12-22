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
    src_label_paths = [path.replace(os.path.splitext(path)[1], ".txt") for path in src_image_paths]
    dst_image_paths = [path.replace("src", "dst").replace(os.path.splitext(path)[1], os.path.splitext(path)[1].lower()) for path in src_image_paths]
    dst_label_paths = [path.replace("src", "dst").replace(os.path.splitext(path)[1], ".txt") for path in src_image_paths]
    return src_image_paths, src_label_paths, dst_image_paths, dst_label_paths


def get_image_size(image_path):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    h_max, w_max = h - 1, w - 1
    return h_max, w_max


def enhance_image(src_image_path, dst_image_path, h_flip, v_flip, hv_flip):
    image = cv2.imread(src_image_path)
    if True:
        # Original image 原图像
        cv2.imwrite(os.path.splitext(dst_image_path)[0]+"-o"+os.path.splitext(dst_image_path)[1], image)
    if h_flip:
        # Flipped Horizontally 图像水平翻转
        h_flip = cv2.flip(image, 1)
        cv2.imwrite(os.path.splitext(dst_image_path)[0]+"-h"+os.path.splitext(dst_image_path)[1], h_flip)
    if v_flip:
        # Flipped Vertically 图像垂直翻转
        v_flip = cv2.flip(image, 0)
        cv2.imwrite(os.path.splitext(dst_image_path)[0]+"-v"+os.path.splitext(dst_image_path)[1], v_flip)
    if hv_flip:
        # Flipped Horizontally & Vertically 图像水平垂直翻转
        hv_flip = cv2.flip(image, -1)
        cv2.imwrite(os.path.splitext(dst_image_path)[0]+"-hv"+os.path.splitext(dst_image_path)[1], hv_flip)


def enhance_label(src_label_path, dst_label_path, h_flip, v_flip, h_v_flip, h, w):
    r_file = open(src_label_path, "r")
    lines = r_file.readlines()
    _, messages = lines[0], lines[1:]
    r_file.close()
    if True:
        # Original label
        o_file = open(os.path.splitext(dst_label_path)[0]+"-o"+os.path.splitext(dst_label_path)[1], "w")
        o_file.writelines(lines[0])
        o_file.writelines(messages)
        o_file.close()
    if h_flip:
        # Flipped Horizontally 水平翻转
        h_file = open(os.path.splitext(dst_label_path)[0]+"-h"+os.path.splitext(dst_label_path)[1], "w")
        h_file.writelines(lines[0])
        for mess in messages:
            if mess.split():
                x1, y1, x2, y2 = map(int, mess.split())
                x1_new = w - x1
                y1_new = y1
                x2_new = w - x2
                y2_new = y2
                new_mess = "{0} {1} {2} {3}\n".format(x1_new, y1_new, x2_new, y2_new)
                h_file.writelines(new_mess)
        h_file.close()
    if v_flip:
        # Flipped Vertically 垂直翻转
        v_file = open(os.path.splitext(dst_label_path)[0]+"-v"+os.path.splitext(dst_label_path)[1], "w")
        v_file.writelines(lines[0])
        for mess in messages:
            if mess.split():
                x1, y1, x2, y2 = map(int, mess.split())
                x1_new = x1
                y1_new = h - y1
                x2_new = x2
                y2_new = h - y2
                new_mess = "{0} {1} {2} {3}\n".format(x1_new, y1_new, x2_new, y2_new)
                v_file.writelines(new_mess)
        v_file.close()
    if hv_flip:
        # Flipped Horizontally & Vertically 水平垂直翻转
        hv_file = open(os.path.splitext(dst_label_path)[0]+"-hv"+os.path.splitext(dst_label_path)[1], "w")
        hv_file.writelines(lines[0])
        for mess in messages:
            if mess.split():
                x1, y1, x2, y2 = map(int, mess.split())
                x1_new = w - x1
                y1_new = h - y1
                x2_new = w - x2
                y2_new = h - y2
                new_mess = "{0} {1} {2} {3}\n".format(x1_new, y1_new, x2_new, y2_new)
                hv_file.writelines(new_mess)
        hv_file.close()


def main(src, dst, h_flip, v_flip, hv_flip):
    dst_check(dst)
    src_image_paths, src_label_paths, dst_image_paths, dst_label_paths = get_path_lists(src)
    for (src_image_path, src_label_path, dst_image_path, dst_label_path) in zip(src_image_paths, src_label_paths, dst_image_paths, dst_label_paths):
        h_max, w_max = get_image_size(src_image_path)
        enhance_image(src_image_path, dst_image_path, h_flip, v_flip, hv_flip)
        enhance_label(src_label_path, dst_label_path, h_flip, v_flip, hv_flip, h_max, w_max)


if __name__ == "__main__":
    SRC = './src'    # dir for origin pics
    DST = './dst'    # dir for resized pics
    h_flip = True    # horizontal
    v_flip = True    # vertical
    hv_flip = True   # both horizontal and vertical
    main(SRC, DST, h_flip, v_flip, hv_flip)
