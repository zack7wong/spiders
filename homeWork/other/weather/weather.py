#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

start_url = 'http://www.tianqihoubao.com/lishi/sanya/month/2018{month}.html'

for month in range(9,13):
    if month < 10:
        month = '0'+str(month)
    url = start_url.format(month=month)
    print(url)
    response = requests.get(url)
    # print(response.text)
    html = HTML(response.text)
    mydates = html.xpath('//div[@id="content"]//tr/td/a/text()')
    tianqis = html.xpath('//div[@id="content"]//tr/td[2]/text()')[1:]
    qiwens = html.xpath('//div[@id="content"]//tr/td[3]/text()')[1:]

    for mydate,tianqi,qiwen in zip(mydates,tianqis,qiwens):

        mydate = mydate.replace('\n','').replace('\r','').replace('\t','')
        tianqi = tianqi.replace('\n','').replace('\r','').replace('\t','')
        qiwen = qiwen.replace('\n','').replace('\r','').replace('\t','')
        # print(mydate,tianqi,qiwen)
        save_res = mydate+','+tianqi+','+qiwen+'\n'
        print(save_res)
        with open('三亚原始数据.csv','a') as f:
            f.write(save_res)
