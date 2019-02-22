#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import config
import download
import os

import re
from lxml.etree import HTML
from lxml.etree import tostring
import math

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "PHPSESSID=fqv82p07s7gfoq51jqs9f5gbe1; Hm_lvt_f719ef2a0af90fabae8f4b23c8b0a340=1550492412; Hm_lpvt_f719ef2a0af90fabae8f4b23c8b0a340=1550750185",
    'Host': "www.wanmi.cc",
    'Pragma': "no-cache",
    'Referer': "http://www.wanmi.cc/zd/qwwn",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
}

def get_domian():
    item_list = []
    with open('zimu.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())
    return item_list

def parse(response):
    html = HTML(response.text)
    div_list = html.xpath('//div[@id="zdlist"]/div[@class="zddiv"]')
    # print(len(div_list))
    for div in div_list:
        link = div.xpath('string(.//div[@class="gsname"]/a/@href)')
        name = re.search('https://www.tianyancha.com/search\?key=(.*?)$', link).group(1)
        # email = div.xpath('string(.//div[@class="other"]/text()[2])').replace('邮箱：','').strip()
        # phone = div.xpath('string(.//div[@class="other"]/text()[3])').replace('电话：','').strip()
        # reg = div.xpath('string(.//div[@class="other"]/text()[4])').replace('注册资本：','').strip()

        deatilText = tostring(div, encoding='utf8').decode('utf8')
        # print(deatilText)

        email = re.search('邮箱：(.*?)<br', deatilText)
        if email:
            email = email.group(1).strip()
        else:
            email = '|'

        phone = re.search('电话：(.*?)<br', deatilText)
        if phone:
            phone = phone.group(1).strip()
        else:
            phone = '|'

        reg = re.search('注册资本：(.*?)注册时间', deatilText)
        if reg:
            reg = reg.group(1).strip()
        else:
            reg = '|'

        save_res = name + '---' + email + '---' + phone + '---' + reg + '\n'
        print(save_res)
        with open('结果.txt','a') as f:
            f.write(save_res)

def start(domain):

    print(domain)
    start_url = 'http://www.wanmi.cc/zd/'+domain
    response = down.get_html(start_url,headers=headers,proxy=True)
    # response = requests.get(start_url, headers=headers)
    # print(response.text)

    #获取总数
    html = HTML(response.text)
    totalCount = int(html.xpath('string(//h1[@class="bt"]/strong[2])'))
    totalPage = math.ceil(totalCount/30)

    print('总数有：'+str(totalCount))
    print('总页数有：'+str(totalPage))

    with open('结果.txt', 'a') as f:
        f.write(domain+'---'+str(totalCount)+'\n')

    #处理第一页
    print('当前页：1')
    parse(response)


    #处理剩余页数
    for i in range(2,totalPage+1):
        print('当前页：'+str(i))
        url = 'http://www.wanmi.cc/zd/'+domain+'?p='+str(i)
        # response = requests.get(url,headers=headers)
        response = down.get_html(url, headers=headers,proxy=True)
        parse(response)


if __name__ == '__main__':
    down = download.Download()
    item_list = get_domian()
    for item in item_list:
        start(item)
