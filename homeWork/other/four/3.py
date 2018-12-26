#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

url = 'http://www.njtech.edu.cn/Home/List/lists/mid/145.html?page={page}'

for i in range(1,16):
    response = requests.get(url.format(page=i))
    html = HTML(response.text)
    titles = html.xpath('//div[@id="mainLeft"]/ul/li/a/text()')
    for title in titles:
        print(title)