#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re


def start():
    saveList = []
    id_list = ['340100000000','340200000000','340300000000','340400000000','340500000000','340600000000','340700000000','340800000000','341000000000','341100000000','341200000000','341300000000','341500000000','341600000000','341700000000','341800000000']
    for id in id_list:
        url = 'http://www.aepb.gov.cn:8080/WRYJG/STZXGK/iframe6.aspx?dsid={id}&wrlx=0'.format(id=id)
        response = requests.get(url)
        html = HTML(response.text)
        # print(response.text)
        urls = html.xpath('//div[@class="jc_list4"]/ul[1]/li/a/@href')
        titles = html.xpath('//div[@class="jc_list4"]/ul[1]/li/a/text()')
        print(titles)
        for link,title in zip(urls,titles):
            saveId = re.search('qySTshow.aspx\?newsid=(\d+)',link)
            if saveId:
                saveId = saveId.group(1)
                if saveId in saveList:
                    continue
                else:
                    saveList.append(saveId)
                    print(saveId,title)
                    save_res = saveId+','+title+'\n'
                    with open('anhui_id.txt','a') as f:
                        f.write(save_res)

if __name__ == '__main__':
    start()