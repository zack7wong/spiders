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
from lxml.etree import HTML

def start(kw):
    oldone_date = time.time() - 86400*30
    startDate = time.strftime('%Y-%m-%d', time.localtime(oldone_date))
    oldmonth_date = time.time() - 86400
    endDate = time.strftime('%Y-%m-%d', time.localtime(oldmonth_date))
    url = 'https://sz.jd.com/industryKeyWord/getIndustrySummDataTrend.ajax?channel=2&date=30{endDate}&endDate={endDate}&kw={kw}&startDate={startDate}'.format(startDate=startDate,endDate=endDate,kw=kw)
    response = requests.get(url,headers=config.HEADERS)
    json_obj = json.loads(response.text)
    avg = round(json_obj['content']['series'][0]['avg'])

    chengjiao_url = 'https://sz.jd.com/industryKeyWord/getKeywordsSummData.ajax?channel=2&date=30{endDate}&endDate={endDate}&kw={kw}&startDate={startDate}'.format(startDate=startDate,endDate=endDate,kw=kw)
    chengjiao_response = requests.get(chengjiao_url, headers=config.HEADERS)
    chengjiao_json_obj = json.loads(chengjiao_response.text)
    chengjiao = chengjiao_json_obj['content']['ConvertRate']['value']
    chengjiao =  str("%.2f"%(float(chengjiao)*100))+'%'

    jd_url = 'https://search.jd.com/Search?keyword={kw}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&psort=3&click=0'.format(kw=kw)
    jd_response = requests.get(jd_url)
    jd_response.encoding = 'utf8'
    html = HTML(jd_response.text)
    jd = html.xpath('string(//span[@id="J_resCount"])')

    print(kw +' 的平均指数是：'+str(avg)+' 成交转化率是：'+chengjiao+' 京东商品数：'+jd)
    with open('results.csv','a') as f:
        write_res = kw+','+str(avg)+','+chengjiao+','+jd+'\n'
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