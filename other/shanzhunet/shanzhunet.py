#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

def start():
    try:
        with open('讯代理.txt') as f:
            IP_URL = f.read().strip()
    except:
        print('缺失文件，请在当前目录下创建 讯代理.txt')
        time.sleep(40000000)





if __name__ == '__main__':
    start()