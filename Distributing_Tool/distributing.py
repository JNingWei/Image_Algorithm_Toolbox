# coding=utf-8

"""
Image_Algorithm_Toolbox
Distribute the files that need to be marked to the designated people, then go to work individually.

__author__ = 'JNingWei'
"""

import logging
import os
import shutil

def dst_check(dst):
    import shutil
    try:
        shutil.rmtree(dst)
    except OSError:
        pass
    os.makedirs(dst)

def main(src, dst, person_names, per_person_per_day):
    dst_check(dst)
    person_num = len(person_names)
    if not os.path.isdir(SRC):
        logging.ERROR('SRC does not exist .')
        exit(1)
    person_folders = []
    for person_name in person_names:
        person_folders.append(os.path.join(DST, person_name))
    for person_folder in person_folders:
        try:
            os.makedirs(person_folder)
        except OSError:
            pass
    src_image_paths = [os.path.join(SRC, name) for name in os.listdir(SRC)
                       if os.path.isfile(os.path.join(SRC, name))]
    src_image_paths.sort()
    per_box = []
    pic_index = 0
    person_index = -1
    for src_image_path in src_image_paths:
        per_box.append(src_image_path)
        pic_index += 1
        if pic_index >= per_person_per_day:
            person_index += 1
            box_num = len(os.listdir(str(person_folders[person_index]))) + 1
            sub_box_path_specify = os.path.join(person_folders[person_index], str(box_num))
            if os.path.exists(sub_box_path_specify):
                logging.ERROR('{} already exists .'.format(sub_box_path_specify))
                exit(1)
            os.mkdir(sub_box_path_specify)
            for per_pic in per_box:
                shutil.copy(per_pic, sub_box_path_specify)

            if person_index >= person_num-1:
                person_index = -1
            per_box = []
            pic_index = 0
    print("\n Distribution has been done ! Go to work now ! ")

if __name__ == "__main__":
    SRC = './src'    # dir for origin pics
    DST = './dst'    # dir for distributed pics
    person_names = ['San.Z', 'Si.L', 'Wu.Z', 'Liu.W']    # member list to be distributed
    per_person_per_day = 5    # the amount of assignments per person per day
    main(SRC, DST, person_names, per_person_per_day)
