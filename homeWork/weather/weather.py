#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

name_list = ['sanya','xian']
start_url = 'http://www.tianqihoubao.com/lishi/{name}/month/2018{month}.html'

for name in name_list:
    for month in range(9,13):
        if month < 10:
            month = '0'+str(month)
        url = start_url.format(month=month,name=name)
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
            if name == 'xian':
                myfilename = '西安原始数据.csv'
            else:
                myfilename = '三亚原始数据.csv'
            with open(myfilename,'a') as f:
                f.write(save_res)
