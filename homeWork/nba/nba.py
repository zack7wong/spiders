#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML

name_list = [{'key':'lebronjames-650','name':'詹姆斯原始数据.txt'},{'key':'kevindurant-1236','name':'杜兰特原始数据.txt'},{'key':'stephencurry-3311','name':'库里原始数据.txt'}]

for name_obj in name_list:
    filename = name_obj['name']
    with open(filename, 'w') as f:
        f.write('')
    url = 'https://nba.hupu.com/players/{name}.html'
    start_url = url.format(name=name_obj['key'])

    response = requests.get(start_url)
    html = HTML(response.text)
    year = html.xpath('//div[@id="in_box"]//table[@class="players_table bott bgs_table"]//tr/td[1]/text()')[1:12]
    changci = html.xpath('//div[@id="in_box"]//table[@class="players_table bott bgs_table"]//tr/td[3]/text()')[1:12]
    mingzhonglv = html.xpath('//div[@id="in_box"]//table[@class="players_table bott bgs_table"]//tr/td[7]/text()')[1:12]
    defen = html.xpath('//div[@id="in_box"]//table[@class="players_table bott bgs_table"]//tr/td[18]/text()')[1:12]
    pingjun_list = html.xpath('//div[@id="in_box"]//table[@class="players_table bott"]//tr[3]/td/text()')[8:13]
    print(year)
    print(changci)
    # for i in range(0,15):
    #     changci[i] = int(changci[i])
    # for i in range(0,15):
    #     changci[i] = int(changci[i])
    print(mingzhonglv)
    print(defen)
    print(pingjun_list)

    with open(filename,'a') as f:
        f.write(str(year)+'\n')
        f.write(str(changci)+'\n')
        f.write(str(mingzhonglv)+'\n')
        f.write(str(defen)+'\n')
        f.write(str(pingjun_list)+'\n')
