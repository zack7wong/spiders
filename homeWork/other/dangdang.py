#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re

price_list = []

for i in range(1,4):
    url = 'http://search.dangdang.com/?key=iphone&act=input&page_index='+str(i)
    response = requests.get(url)
    html = HTML(response.text)
    # print(response.text)
    names = html.xpath('//div[@id="search_nature_rg"]/ul/li//p[@class="link"]/a/text()|//div[@id="search_nature_rg"]/ul/li//p[@class="dang"]/a/text()')
    prices = html.xpath('//div[@id="search_nature_rg"]/ul/li//p[@class="price"]//span/text()')
    comments = html.xpath('//div[@id="search_nature_rg"]/ul/li//p[@class="star"]//a/text()')

    for name,price,comment in zip(names,prices,comments):
        # print(name,price,comment)
        price = price[1:]
        price_list.append(float(price))
        comment = price[:-3]
        print(name, price, comment)
        res = name+','+price+','+comment+'\n'
        with open('results.txt','a') as f:
            f.write(res)

#数据计算
print('最大值是：'+str(max(price_list)))
print('最小值是：'+str(min(price_list)))
print('平均值是：'+str(sum(price_list)/len(price_list)))