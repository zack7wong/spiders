#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

num = 1
url = 'http://search.dangdang.com/?key=%CA%E9%BC%AE&act=input&page_index={page}'
with open('results.csv','w') as f:
    f.write('序号,书名,价格,评论数\n')

for i in  range(1,40):
    start_url = url.format(page=i)
    response = requests.get(start_url)
    # print(response.text)
    html = HTML(response.text)
    titles = html.xpath('//div[@id="search_nature_rg"]/ul/li//a[@name="itemlist-title"]/@title')
    prices = html.xpath('//div[@id="search_nature_rg"]/ul/li//span[@class="search_now_price"]/text()')
    comments = html.xpath('//div[@id="search_nature_rg"]/ul/li//a[@class="search_comment_num"]/text()')
    # print(titles)
    # print(prices)
    # print(comments)
    for title,price,comment in zip(titles,prices,comments):
        title = title.replace(',','，').replace('\n','').strip()
        save_res = str(num)+','+title+','+price+','+comment+'\n'
        print(save_res)
        with open('results.csv','a') as f:
            f.write(save_res)
        num+=1