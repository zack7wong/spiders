#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     run
   Description :
   Author :        hayden_huang
   Date：          2018/11/20 14:43
-------------------------------------------------
"""

import config
import download

def start(pageToken):
    start_url = config.START_URL.format(pageToken=pageToken)
    print(start_url)
    response = down.get_html(start_url)
    if(response.status_code == 200):
        print('该链接有效')
        with open('results.txt','a') as f:
            write_res = start_url+'\n'
            f.write(write_res)
    else:
        print('无效')

if __name__ == '__main__':
    down= download.Download()
    startnum = int(input('请输入开始值：'))
    endnum = int(input('请输入末尾值：'))
    for i in range(startnum,endnum):
        start(str(i))