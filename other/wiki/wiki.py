#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
from urllib.parse import unquote
import os
import re

url = 'https://zh.wikipedia.org/wiki/Category:%E7%BE%8E%E5%9C%8B%E5%90%84%E5%85%AC%E5%8F%B8%E4%BA%BA%E7%89%A9'

proxies = {
    'https':'http://127.0.0.1:1087'
}
response = requests.get(url,verify=False,proxies=proxies)
# print(response.text)

html = HTML(response.text)
url_list = html.xpath('//div[@class="mw-category"]/div//ul/li//a/@href')
for url in url_list:
    link = 'https://zh.wikipedia.org'+url
    # print(link)
    detail_response = requests.get(link,verify=False,proxies=proxies)
    detail_html = HTML(detail_response.text)
    detail_url_list = detail_html.xpath('//div[@class="mw-category"]/div//ul/li//a/@href')
    for endurl in detail_url_list:
        endlink = 'https://zh.wikipedia.org' + endurl
        print(endlink)
        try:
            end_response = requests.get(endlink,verify=False,proxies=proxies)
            name = re.search('https://zh.wikipedia.org/wiki/(.*?)$',endlink).group(1)
            file_name = unquote(name) + '.html'
            file_name = file_name.replace('/','-')
            print(file_name)
            save_file = os.path.join('html',file_name)
            with open(save_file,'w') as f:
                f.write(end_response.text)
        except:
            print('error...')
            with open('error.txt','a') as f:
                f.write(endlink+'\n')
