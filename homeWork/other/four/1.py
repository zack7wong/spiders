#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

url = 'http://jwb.njtech.edu.cn/'
response = requests.get(url)
response.encoding = 'gbk'
html = HTML(response.text)
titles = html.xpath('//div[@id="status1"]//tr/td/a/@title')
for title in titles:
    print(title)