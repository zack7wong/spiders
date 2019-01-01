#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "UM_distinctid=16764767684676-01212373df9155-35627600-1fa400-16764767685243; cityPy_expire=1546939107; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1546334309; cityPy=shihezi; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1546341929",
    'Host': "lishi.tianqi.com",
    'Pragma': "no-cache",
    'Referer': "http://lishi.tianqi.com/tacheng/index.html",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "5fffd8c8-89b0-4868-99fc-6b4a65fc3331"
    }

year_list = ['2013','2014','2015','2016','2017']
start_url = 'http://lishi.tianqi.com/tacheng/{date}.html'

for year in year_list:
    filename = '塔城'+year+'.csv'
    for month in range(1,13):
        if month < 10:
            month = '0'+str(month)
        month = str(month)
        date = year+month
        url = start_url.format(date=date)
        print(url)
        response = requests.get(url,headers=headers)
        response.encoding = 'gbk'
        html = HTML(response.text)
        mydates = html.xpath('//div[@class="tqtongji2"]/ul/li/a/text()')
        max_qiwens = html.xpath('//div[@class="tqtongji2"]/ul/li[2]/text()')[1:]
        min_qiwens = html.xpath('//div[@class="tqtongji2"]/ul/li[3]/text()')[1:]
        tianqis = html.xpath('//div[@class="tqtongji2"]/ul/li[4]/text()')[1:]
        fengxiangs = html.xpath('//div[@class="tqtongji2"]/ul/li[5]/text()')[1:]
        fenglis = html.xpath('//div[@class="tqtongji2"]/ul/li[6]/text()')[1:]

        for mydate,max_qiwen,min_qiwen,tianqi,fengxiang,fengli in zip(mydates,max_qiwens,min_qiwens,tianqis,fengxiangs,fenglis):
            save_res = mydate+','+max_qiwen+','+min_qiwen+','+tianqi+','+fengxiang+','+fengli+'\n'
            print(save_res)
            with open(filename,'a') as f:
                f.write(save_res)