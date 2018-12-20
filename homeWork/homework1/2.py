#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import requests
import re

html = requests.get('https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%A3%8E%E6%99%AF&oq=%E9%A3%8E%E6%99%AF&rsp=-1').text
reg = r'src="(//.*?\.png)"'
imgre = re.compile(reg)
imgList = re.findall(imgre, html)
x = 0
for imgurl in imgList:
    imgurl = "http:"+imgurl
    print('正在下载：'+imgurl)
    urllib.request.urlretrieve(imgurl, 'img/%s.png' % x)
    x += 1