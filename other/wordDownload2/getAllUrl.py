#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import random
import download
import redis
import json

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Host': "www.gezhongshu.com",
    'Pragma': "no-cache",
    # 'Proxy-Authorization': "Basic SklBTllJSFRUMTpLSUZLT1lZODRK",
    # 'Proxy-Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    # 'Postman-Token': "60e23350-dd5c-4549-8e77-8d5469e9c238"
}


def parse_detail(url):
    print(url)
    response = down.get_html(url, headers=headers)
    # print(response.text)
    html = HTML(response.text)

    bookType = html.xpath('string(//div[@class="pattl"]/ignore_js_op[1]/div[@class="ik_vt_down"]//td[1]/img/@src)')
    bookType = re.search('image/filetype/(.*?)\.png',bookType)
    if bookType:
        bookType = bookType.group(1)
        if bookType == 'azw':
            bookType = 'azw3'
    else:
        bookType = ''

    link = html.xpath('string(//div[@class="pattl"]/ignore_js_op[1]/div[@class="ik_vt_down"]//td[6]/a/@href)')
    if link != '':
        link = 'http://www.gezhongshu.com/'+link

    name =  html.xpath('string(//span[@id="thread_subject"])')
    name = re.search('(《.*?》)',name)
    if name:
        name = name.group(1)
    else:
        name = ''

    doubanId = re.search('book.douban.com/subject/(\d+)/',response.text)
    if doubanId:
        doubanId = doubanId.group(1)
    else:
        doubanId = ''

    classname = html.xpath('string(//div[@class="forum_tit_vie"]/h3/a)')

    save_res = name+'||'+doubanId+'||'+classname+'||'+url+'||'+bookType+'||'+link+'\n'
    save_res = save_res.replace(',','，').replace('||',',')
    print(save_res)
    with open('结果.csv','a') as f:
        f.write(save_res)

    obj = {
        'name':name,
        'doubanId':doubanId,
        'classname':classname,
        'url':url,
        'bookType':bookType,
        'link':link,
    }
    myredisCli.rpush('bookObj_task',json.dumps(obj))


def get_each_cat(url):
    response = down.get_html(url, headers=headers)
    # print(response.text)
    html = HTML(response.text)

    allNumPage = html.xpath('string(//div[@class="pg"]/a[last()-1])')
    allNumPage = int(re.search('(\d+)',allNumPage).group(1))
    print('总页数：'+str(allNumPage))
    detail_url_list = html.xpath('//ul[@class="bud"]/li/a/@href')
    for detail_url in detail_url_list:
        detail_url = 'http://www.gezhongshu.com/'+detail_url
        parse_detail(detail_url)

    for i in range(2,allNumPage+1):
        try:
            print('当前页：'+str(i))
            each_url = url + '&page=' + str(i)
            print(each_url)
            response = down.get_html(each_url, headers=headers)
            # print(response.text)
            html = HTML(response.text)
            detail_url_list = html.xpath('//ul[@class="bud"]/li/a/@href')
            for detail_url in detail_url_list:
                try:
                    detail_url = 'http://www.gezhongshu.com/' + detail_url
                    parse_detail(detail_url)
                except:
                    print('详情页出错')
                    with open('详情页出错url.txt','a') as f:
                        f.write(detail_url+'\n')
                    continue
        except:
            print('翻页出错')
            each_url = url + '&page=' + str(i)
            with open('翻页页出错url.txt', 'a') as f:
                f.write(each_url + '\n')
            continue



if __name__ == '__main__':
    down = download.Download()
    myredisCli = redis.Redis()
    url = 'http://www.gezhongshu.com/forum.php'
    response = down.get_html(url,headers=headers)
    # print(response.text)
    html = HTML(response.text)
    index_url_list = html.xpath('//div[@id="category_1"]//td[@class="fl_g"]/dl/dt/a/@href')
    for index_url in index_url_list:
        try:
            link = 'http://www.gezhongshu.com/'+index_url
            print('当前分类url：')
            print(link)
            get_each_cat(link)
        except:
            print('分类页出错')
            link = 'http://www.gezhongshu.com/' + index_url
            with open('分类页出错url.txt', 'a') as f:
                f.write(link + '\n')
            continue
