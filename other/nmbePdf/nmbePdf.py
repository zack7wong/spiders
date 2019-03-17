#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import urllib
import re
import os

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'cookie': "_ga=GA1.2.954549164.1552822222; _gid=GA1.2.2103385567.1552822222; WSCSESSID=o6tcp6lllvkks8bvjmsbreg8u5; _gat=1",
    'pragma': "no-cache",
    'referer': "https://wsc.nmbe.ch/bibliography",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

proxies = {
    'http':'http://127.0.0.1:1087',
    'https':'http://127.0.0.1:1087'
}

def start(year,dicPath):
    start_url = 'https://wsc.nmbe.ch/listbib/'+year
    response = requests.get(start_url, headers=headers, verify=False,proxies=proxies)
    # print(response.text)
    html = HTML(response.text)
    p_list = html.xpath('//div[@class="reference"]/p')
    for p in p_list:
        url = p.xpath('string(./a[@class="pdfdown"]/@href)')
        fileNameStr = p.xpath('string(./text())')
        fileNameRe = re.search('^(.*?\(.*?\)).',fileNameStr)
        if fileNameRe:
            fileName = fileNameRe.group(1)+'.pdf'
        else:
            print('error')
            continue

        link = 'https://wsc.nmbe.ch' + url
        print('正在下载：'+fileName)
        print(link)
        savePath = os.path.join(dicPath,fileName)
        if os.path.exists(savePath):
            print('已经下载过了')
            continue

        # urllib.request.urlretrieve(link, savePath)
        try:
            down_response = requests.get(link,headers=headers,verify=False,proxies=proxies)
        except:
            print('error...')
            continue

        with open(savePath,'wb') as f:
            f.write(down_response.content)


if __name__ == '__main__':
    print('[1].1757-1897')
    print('[2].1898-1934')
    print('[3].1935-1959')
    print('[4].1960-1969')
    print('[5].1970-1980')
    print('[6].1981-1987')
    print('[7].1988-1991')
    print('[8].1992-1995')
    print('[9].1996-1999')
    print('[10].2000-2004')
    print('[11].2005-2009')
    print('[12].2010-2014')
    print('[13].2015-2019')

    year = input('请输入要下载的年份：')


    year_list = [{'year':'1','name':'1757-1897'},{'year':'2','name':'1898-1934'},{'year':'3','name':'1935-1959'},{'year':'4','name':'1960-1969'},{'year':'5','name':'1970-1980'},{'year':'6','name':'1981-1987'},{'year':'7','name':'1988-1991'},{'year':'8','name':'1992-1995'},{'year':'9','name':'1996-1999'},{'year':'10','name':'2000-2004'},{'year':'11','name':'2005-2009'},{'year':'12','name':'2010-2014'},{'year':'13','name':'2015-2019'}]
    dicPath = ''
    for each in year_list:
        if each['year'] == year:
            pwd = os.getcwd()
            path = os.path.join(pwd, each['name'])
            dicPath = path
            folder = os.path.exists(path)
            if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(path)
            break


    start(year,dicPath)