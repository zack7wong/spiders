#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
# from lxml.etree import HTML
import re

item_list = []
with open('urls.txt') as f:
    results = f.readlines()
    for res in results:
        item_list.append(res.strip())

for myurl in item_list:
    url = 'http://www.wanmi.cc/gj/'+myurl
    print(url)
    response = requests.get(url)
    # html = HTML(response.text)
    # price = html.xpath('string(//div[@class="gujia"]/text())')
    # res = re.search('(\d+)',price).group(1)
    res = re.search('<div class="gujia">¥ (.*?) 元</div>',response.text).group(1)
    print(myurl+'----'+res)
    with open('结果.txt','a') as f:
        save_res = myurl+'----'+res+'\n'
        f.write(save_res)


