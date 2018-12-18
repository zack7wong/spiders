#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
from lxml.etree import HTML

#请求头
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'cookie': "__mta=151811974.1542774057457.1542776867374.1544772873949.7; uuid_n_v=v1; uuid=D6F77220ED4411E8A50EC9D5D894D3828347BEB7BC7B4E9EBF735B0C705849B4; _lxsdk_cuid=167347fe8e8c8-0f68dac8d116bc-35637400-1fa400-167347fe8e9c8; _lxsdk=D6F77220ED4411E8A50EC9D5D894D3828347BEB7BC7B4E9EBF735B0C705849B4; _csrf=d0cb0096bfef7d8b1fe19ce3106c3a21a321ebc7efb3e2780615171150499ae3; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; __mta=151811974.1542774057457.1542776867374.1544772859278.7; _lxsdk_s=167aba32a2f-22c-6f5-d8a%7C%7C8",
    'pragma': "no-cache",
    'referer': "https://maoyan.com/board/4",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    }

#for循环翻页
for i in range(10):
    url = 'https://maoyan.com/board/4?offset='+str(i*10)
    #发送请求
    response = requests.get(url,headers=headers)
    #得到结果，用lxml解析
    html = HTML(response.text)
    #xpath获取结果
    titles = html.xpath('//dl[@class="board-wrapper"]/dd/a/@title')
    names = html.xpath('//dl[@class="board-wrapper"]//p[@class="star"]/text()')
    times = html.xpath('//dl[@class="board-wrapper"]//p[@class="releasetime"]/text()')
    #结果合并
    for title,name,time in zip(titles,names,times):
        res = title+','+name.strip()+','+time.strip()+'\n'
        print(res)
        #写文件
        with open('maoyan.csv','a') as f:
            f.write(res)