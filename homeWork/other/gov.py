#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
from lxml.etree import HTML

#初始url
URL = 'http://sousuo.gov.cn/column/40123/{page}.htm'

#翻页
for i in range(0,11):
    start_url = URL.format(page=i)
    print(start_url)
    #发送请求
    response = requests.get(start_url)

    #lxml解析获得的结果
    html = HTML(response.text)

    #获取url和标题
    urls = html.xpath('//ul[@class="listTxt"]/li/h4/a/@href')
    titles = html.xpath('//ul[@class="listTxt"]/li/h4/a/text()')


    #对结果进行拼接
    for url,title in zip(urls,titles):
        print(url,title)
        with open('结果.txt','a') as f:
            f.write(url+','+title+'\n')