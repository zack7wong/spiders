#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
from lxml.etree import HTML
import re

#网站url
url = 'https://www.whu.edu.cn/'

#request请求
response = requests.get(url)
#设置编码
response.encoding='utf8'

#lxml解析返回的结果
html = HTML(response.text)

#xpath获取对应的数据
lis = html.xpath('//a/@href')
titles = html.xpath('//a/text()')

for li,title in zip(lis,titles):
    #对不匹配的数据剔除
    title = title.strip()
    if title !='':
        #re正则表达式匹配
        if re.match('http://news.*?|info',li):
            #只获取新闻内容
            if li[:4] == 'info':
                link = 'https://www.whu.edu.cn/'+li
            else:
                link = li
            print(link,title)