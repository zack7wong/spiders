#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     domainCheck
   Description :
   Author :        hayden_huang
   Date：          2018/12/15 22:37
-------------------------------------------------
"""


import multiprocessing
from multiprocessing import Pool
import time
import re


def read_txt():
    account_list = []

    with open('urls.txt') as f:
        results = f.readlines()
        for res in results:
            try:
                account_list.append(res.strip())
            except:
                print('该行文本格式有误')
                print(res)
                with open('格式错误.txt', 'a') as ff:
                    ff.write(res)
    return account_list

def get_res(account_list,num):
    for url in account_list:
        if re.match('(http|https)://(.*?)/',url):
            res = re.match('(http|https)://(.*?)/',url).group(2)
            if res not in all_list:
                allres_list.append(res)
        else:
            with open('failed.txt', 'a') as f:
                f.write(res.strip() + '\n')


if __name__ == '__main__':
    print('程序正在运行。。。')
    multiprocessing.freeze_support()
    with multiprocessing.Manager() as MG:
        allres_list = multiprocessing.Manager().list()

    num = '5'
    account_list = read_txt()
    zhu_num = int(len(account_list)/int(num))
    all_list = [account_list[i:i + zhu_num] for i in range(0, len(account_list), zhu_num)]

    item_list = []
    for each in all_list:
        tuple_each =(each,all_list.index(each))
        item_list.append(tuple_each)

    args = tuple(item_list)
    p = multiprocessing.Pool(int(num))
    for arg in args:
        p.apply_async(get_res, args=arg)
    p.close()
    p.join()

    allres_list = list(set(allres_list))
    for res in allres_list:
        with open('results.txt', 'a') as f:
            f.write(res.strip() + '\n')
    print('总数为：'+str(len(account_list)))
    print('去重后为：'+str(len(allres_list)))
    print('10秒后关闭....')
    time.sleep(10)