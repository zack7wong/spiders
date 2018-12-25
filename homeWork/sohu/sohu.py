#!/usr/bin/env python
# -*- coding:utf-8 -*-


#导入包
import requests
from lxml.etree import HTML
import urllib
import re
import matplotlib.pyplot as plt
import os
import time as time




#起始url

url = 'http://news.sohu.com/'
response = requests.get(url)

#lxml解析结果

html = HTML(response.text)
print(response.text)
urls = html.xpath('//div[@class="focus-news"]//li/a/@href')
# titles = html.xpath('//div[@class="focus-news"]//li/a/@title')

#初始化写文件
with open('results.txt', 'w') as f:
    f.write('')

for url in urls:
    print(url)
    response = requests.get(url)
    html = HTML(response.text)
    content = html.xpath('//article[@class="article"]/p/text()')
    content = ''.join(content)
    title = html.xpath('string(//h1)')

    with open('results.txt', 'a') as f:
        f.write(content)
