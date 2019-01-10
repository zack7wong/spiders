#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     domainCheck_dan
   Description :
   Author :        hayden_huang
   Date：          2018/12/16 11:47
-------------------------------------------------
"""
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

def get_res(account_list):
    for url in account_list:
        if re.match('(http|https)://(.*?)/',url):
            res = re.match('(http|https)://(.*?)/',url).group(2)
            if res not in all_list:
                all_list.append(res)
        else:
            with open('failed.txt', 'a') as f:
                f.write(url.strip() + '\n')


if __name__ == '__main__':
    print('程序正在运行。。。')
    all_list = []

    account_list = read_txt()
    get_res(account_list)

    for res in all_list:
        with open('results.txt', 'a') as f:
            f.write(res.strip() + '\n')
    print('总数为：'+str(len(account_list)))
    print('去重后为：'+str(len(all_list)))
    print('10秒后关闭....')
    time.sleep(10)