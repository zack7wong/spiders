#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import urllib
import os
import db

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "SID=jct9g6ip2gji0980ip0c8olpl0",
    'Host': "virusshare.com",
    'Pragma': "no-cache",
    'Referer': "https://virusshare.com/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'cache-control': "no-cache",
}

proxies = {
    'http':'http://127.0.0.1:1087',
    'https':'http://127.0.0.1:1087',
}

def login():
    print('正在登录。。')
    url = 'https://virusshare.com/'
    response = requests.get(url,headers=headers,proxies=proxies)
    responseCookie = response.cookies.get_dict()
    headers['Cookie'] = 'SID='+responseCookie['SID']
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    login_url = 'https://virusshare.com/processlogin.4n6'
    data = 'username=hs&password=XZvZCdIvDmys'

    response = requests.post(login_url,headers=headers,data=data,proxies=proxies)
    # print(response.text)

def get_info(kw):
    print('当前查找病毒类型：'+kw)
    #名称，文件类型；上传时间，简介，路径
    url = 'https://virusshare.com/search.4n6'

    for i in range(20):
        try:
            pageToken = i*20
            body = 'search={kw}&start={pageToken}'
            data = body.format(kw=kw,pageToken=pageToken)
            response = requests.post(url, headers=headers, data=data,timeout=30,proxies=proxies)
            html = HTML(response.text)

            # print(response.text)
            talbe_list = html.xpath('//table')
            for table in talbe_list:
                try:
                    virusName = ''
                    virusType = kw
                    uploadTime = table.xpath('string(.//tr[last()-1]/td/text())')
                    uploadTime = uploadTime.replace('submitted','').replace('UTC','').strip()
                    description = table.xpath('string(.//tr//pre/text())')
                    description = description.replace('\n',' ').replace('\t',' ')

                    #下载文件
                    downUrl = 'https://virusshare.com/' + table.xpath('string(.//tr[1]/td[1]/a/@href)')
                    MD5_str = table.xpath('string(.//tr[1]/td[3]/text())')
                    fileName = 'VirusShare_'+MD5_str+'.zip'
                    saveFilePath = os.path.join('virusFile',fileName)
                    # urllib.request.urlretrieve(downUrl,saveFilePath)

                    print('正在下载：' + fileName)
                    response = requests.get(downUrl,headers=headers,timeout=60,proxies=proxies)
                    with open(saveFilePath,'wb') as f:
                        f.write(response.content)

                    filePath = 'virusFile/'+fileName

                    sql = "insert into virus2(virusName,virusType,uploadTime,description,filePath) values ('%s','%s','%s','%s','%s')"%(virusName,virusType,uploadTime,description,filePath)+"ON DUPLICATE KEY UPDATE uploadTime='%s'" % (uploadTime)
                    print(sql)
                    dbClient.save(sql)
                except:
                    print('error')
                    continue

            if 'No additional results available' in response.text:
                break

        except:
            print('error')
            continue



def start():
    login()
    searchKey_list = ['worm','win32','win95','PE']
    for kw in searchKey_list:
        get_info(kw)


if __name__ == '__main__':
    dbClient = db.MysqlClient()
    start()