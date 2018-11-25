#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import imghdr


def delimg(img_name,type=None):
    pwd = os.getcwd()
    rootdir = pwd
    list = os.listdir(rootdir)
    for line in list:
        imgType = imghdr.what(line)
        if imgType:
            filepath = os.path.join(rootdir, line)
            if type=='list':
                if line in img_name:
                    continue
                else:
                    print('正在删除:' + line)
                    os.remove(filepath)
            else:
                if line == img_name:
                    continue
                else:
                    print('正在删除:' + line)
                    os.remove(filepath)

def read_txt():
    img_name_list = []
    with open('images.txt') as f:
        results = f.readlines()
        for res in results:
            img_name = res.strip()
            img_name_list.append(img_name)
    return img_name_list

if __name__ == '__main__':
    while True:
        img_name = input('请输入要保留的图片名称(eg: aa.jpg  如需批量请输入 all)：')
        if img_name == 'all':
            img_name_list = read_txt()
            delimg(img_name_list, type='list')
        else:
            delimg(img_name)