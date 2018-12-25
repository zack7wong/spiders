#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     wordDownload
   Description :
   Author :        hayden_huang
   Date：          2018/12/23 17:30
-------------------------------------------------
"""

import requests
import download
import re

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Host': "www.well1000.cn",
    'Pragma': "no-cache",
    'Proxy-Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'cache-control': "no-cache",
    'Referer': "http://www.well1000.cn/",
}

def get_cookie():
    response = down.get_html(url, headers=headers,timeout=30)
    print(response.text)
    id = re.search('SetC\("id", "(.*?)"\)', response.text, re.S).group(1)
    mycookie = response.cookies.get_dict()
    mycookieStr = 'title=' + mycookie['title'] + '; '
    # mycookieStr += 'safedog-flow-item=' + mycookie['safedog-flow-item'] + '; '
    mycookieStr += 'id=' + id + ';'
    print(mycookieStr)
    headers['cookie'] = mycookieStr

def download_word(url):
    response = requests.get(url,headers=headers,timeout=30)
    res = re.search('本地下载链接：</b><a href=\\\\"(.*?)\\\\"',response.text,re.S).group(1)
    name = re.search('本地下载链接：</b><a href=\\\\"(.*?)\\\\".*?>(.*?)</a>',response.text,re.S).group(2)
    print(name)
    # id = re.search('SetC\("id", "(.*?)"\)',response.text,re.S).group(1)
    link = 'http://www.well1000.cn'+res
    print(link)
    # mycookie = response.cookies.get_dict()
    # print(mycookie)
    # mycookieStr = 'title='+mycookie['title']+'; '
    # mycookieStr += 'safedog-flow-item='+mycookie['safedog-flow-item']+'; '
    # mycookieStr += 'id=' + id + ';'
    # print(mycookieStr)

    # headers['cookie'] = mycookieStr

    with open('cookie.txt') as f:
        headers['cookie'] = f.read()

    # headers['cookie'] = 'title=75j4j82f6; id=b4g5cj2i3g;'
    while True:
        response = down.get_html(link,headers=headers,allow_redirects=False,timeout=30)
        print(response.status_code)
        if response.status_code==302:
            get_cookie()
            # headers['cookie'] = mycookieStr

        if response.status_code==200:
            with open('cookie.txt','w') as f:
                f.write(headers['cookie'])
            break

    filename= name+'.doc'
    with open(filename, 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    down = download.Download()
    item_list = []
    with open('url.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())

    for url in item_list:
        try:
            print('正在下载：'+url)
            download_word(url)
        except:
            print('未知错误')


