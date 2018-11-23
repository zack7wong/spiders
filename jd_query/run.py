#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     run
   Description :
   Author :        hayden_huang
   Date：          2018/11/23 15:25
-------------------------------------------------
"""

import download
import time
import requests
import config
import json
import math


def start(kw):
    oldone_date = time.time() - 86400*30
    startDate = time.strftime('%Y-%m-%d', time.localtime(oldone_date))
    oldmonth_date = time.time() - 86400
    endDate = time.strftime('%Y-%m-%d', time.localtime(oldmonth_date))
    url = 'https://sz.jd.com/industryKeyWord/getIndustrySummDataTrend.ajax?channel=2&date=30{endDate}&endDate={endDate}&kw={kw}&startDate={startDate}'.format(startDate=startDate,endDate=endDate,kw=kw)
    response = requests.get(url,headers=config.HEADERS)
    json_obj = json.loads(response.text)
    avg = round(json_obj['content']['series'][0]['avg'])
    print(kw +' 的平均指数是：'+str(avg))
    with open('results.csv','a') as f:
        write_res = kw+','+str(avg)+'\n'
        f.write(write_res)


if __name__ == '__main__':
    down = download.Download()
    with open('results.csv','w') as f:
        f.write('')
    while True:
        kw = input('请输入要查询的关键词(如需批量请输入  all)：')
        if kw == 'all':
            with open('keyword.txt') as f:
                results = f.readlines()
                for res in results:
                    kw = res.strip()
                    start(kw)
        else:
            start(kw)