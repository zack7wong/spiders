#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

with open('fujian_id.txt') as f:
    results = f.readlines()
    for res in results:
        url = res.split(',')[0]
        title = res.split(',')[1].strip()

        response = requests.get(url)
        html = HTML(response.text)
        new_url = html.xpath('string(//div[@class="leftBox"]/div[@class="content bottom10"]//li[last()]/a/@href)')
        new_url = 'http://wryfb.fjemc.org.cn/' + new_url
        save_res = new_url.strip() + ',' + title.strip() + '\n'
        print(save_res)
        with open('fujian_id2.txt', 'a') as f:
            f.write(save_res)