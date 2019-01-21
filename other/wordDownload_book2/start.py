#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import re
import random
import download
import redis
import json
import os
import time

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

def bookDownload(item):
    try:
        saveFileName = item['name'].replace('《','').replace('》','') + '.' + item['bookType']
        savePath = os.path.join('books', saveFileName)
        print('正在下载：'+saveFileName)
        print(item['link'])

        cookie =  {'Cookie': "9090_2132_saltkey=u1d9pIe9; 9090_2132_lastvisit=1547367467; UM_distinctid=1684680b76e1f0-0cb0c6befd2c36-10376654-1fa400-1684680b77049; 9090_2132_atarget=1; 9090_2132_visitedfid=75; 9090_2132_auth=99c2KOxym7hLmnorZIBxp0WCVFpmxBIuum7hrUt%2BEbILaouzdHbOrqqqqsP0DFaHrpiIk4ZGKGL3euxjmEfp5ncN; 9090_2132_lastcheckfeed=8929%7C1547380549; 9090_2132_smile=1D1; 9090_2132_st_t=8929%7C1547382895%7C61519a8fe76761a103235d886da7ebb9; 9090_2132_forum_lastvisit=D_75_1547382895; 9090_2132_security_cookiereport=8aee7ciHUw0owv2e00Stl96chxXJBRWHy59KBeyamnDxr2GJCzIO; 9090_2132_pc_size_c=0; 9090_2132_ulastactivity=e36cllLhXr75zV90Yx0z0ixFhjn5UL0mT7DAM3ovEFq63oYzqE2A; CNZZDATA1273035633=560660413-1547370433-%7C1547640439; 9090_2132_sid=DZAFdl; 9090_2132_lip=223.100.161.80%2C1547643415; 9090_2132_lastact=1547644480%09forum.php%09viewthread; 9090_2132_st_p=8929%7C1547644480%7Cf3bdab6587ceb790f8f733ffbf689def; 9090_2132_viewid=tid_476"}
        headers.update(cookie)
        response = down.get_html(item['link'], headers=headers)
        with open(savePath, 'wb') as file:
            file.write(response.content)
        print('下载成功')
        with open('下载成功.txt', 'a') as f:
            f.write(str(item) + '\n')
    except:
        print('出错。。' + str(item))
        with open('下载出错.txt', 'a') as f:
            f.write(str(item) + '\n')

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
        return

    link = html.xpath('string(//div[@class="pattl"]/ignore_js_op[1]/div[@class="ik_vt_down"]//td[6]/a/@href)')
    if link != '':
        link = 'http://www.gezhongshu.com/'+link

    name =  html.xpath('string(//span[@id="thread_subject"])')
    name = re.search('(《.*?》)',name)
    if name:
        name = name.group(1)
    else:
        return

    doubanId = re.search('book.douban.com/subject/(\d+)/',response.text)
    if doubanId:
        doubanId = doubanId.group(1)
    else:
        doubanId = ''

    classname = html.xpath('string(//div[@class="forum_tit_vie"]/h3/a)')

    save_res = name.strip()+'||'+doubanId+'||'+classname+'||'+url+'||'+bookType+'||'+link+'\n'
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

    bookDownload(obj)
    # myredisCli.rpush('bookObj_task',json.dumps(obj))


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

# 540529113@qq.co  xinfei123