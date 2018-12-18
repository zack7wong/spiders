#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import json
import re
import os
import config
import time
import query
import multiprocessing
from multiprocessing import Pool
import read

if __name__ == '__main__':
    print('程序正在运行。。。')
    multiprocessing.freeze_support()

    reader = read.Read()
    url_list = reader.read_txt()
    queryer = query.Query()
    # for domain_obj in url_list:
    #     print('正在查询该链接是否已注册： '+domain_obj['url'])
    #     queryer.query_regist(domain_obj)

    num = 10
    zhu_num = int(len(url_list) / int(num))
    all_list = [url_list[i:i + zhu_num] for i in range(0, len(url_list), zhu_num)]

    item_list = []
    for each in all_list:
        tuple_each = (each, all_list.index(each))
        item_list.append(tuple_each)

    args = tuple(item_list)
    p = multiprocessing.Pool(int(num))
    for arg in args:
        p.apply_async(queryer.query_regist, args=arg)
    p.close()
    p.join()

    print('程序已结束')
