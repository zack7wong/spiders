#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml.etree import HTML
import json
import math

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "91",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "ASP.NET_SessionId=c4xqr445yr2n1pyx10pjiq55",
    # 'Host': "219.147.6.195:8403",
    # 'Origin': "http://219.147.6.195:8403",
    'Pragma': "no-cache",
    # 'Referer': "http://219.147.6.195:8403/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}

ip_list = ['221.214.107.80:8403','219.147.6.195:8403','60.210.111.130:8406','218.56.152.39:8403','221.2.232.50:8401','120.220.248.146:8403','122.4.213.20:8403','60.211.254.236:8403','220.193.65.234:8403','60.212.191.18:8408','219.146.185.5:8404','218.56.160.167:8403','58.57.43.244:8414','222.133.11.150:8403','222.175.25.10:8403','222.134.12.94:8403','219.146.175.226:8403']
year_list = ['2014','2015','2016','2017','2018','2019']
def start():
    item_list = []
    id_list = []
    for ip in ip_list:
        for year in year_list:
            url = 'http://{ip}/ajax/npublic/Index.ashx'
            start_url = url.format(ip=ip)
            print(start_url)
            body = 'IsBeginZxjc=2&isgk=2&Method=LoadGrid&SubType=0&Year={year}&areaCode=0&EntName=&page={pageToken}&rows=100'

            #获取第一页
            data = body.format(year=year, pageToken=1)
            try:
                response = requests.post(start_url, data=data, headers=headers, timeout=15)
            except:
                continue
            print(response.text)
            if response.text[0] == '(' and response.text[-1] == ')':
                json_obj = json.loads(response.text[1:-1])
            else:
                json_obj = json.loads(response.text)

            if json_obj['total'] == 0:
                continue

            #处理第一页
            for item in json_obj['rows']:
                CityCode = item['CityCode']
                CityName = item['CityName']
                AreaCode = item['AreaCode']
                AreaName = item['AreaName']
                EntCode = item['EntCode']
                EntName = item['EntName']
                EntTypeName = item['EntTypeName']
                obj = {
                    'ip':ip,
                    'CityCode':CityCode,
                    'CityName':CityName,
                    'AreaCode':AreaCode,
                    'AreaName':AreaName,
                    'EntCode':EntCode,
                    'EntName':EntName,
                    'EntTypeName':EntTypeName,
                }
                for key in obj.keys():
                    if obj[key] == None:
                        obj[key] = ''
                if EntCode not in id_list:
                    item_list.append(obj)
                    id_list.append(EntCode)


            #获取总页数
            totalPage = math.ceil(json_obj['total']/100)

            #处理剩余页数
            for i in range(2,totalPage+1):
                print('当前页：'+str(i))
                data = body.format(year=year, pageToken=i)
                try:
                    response = requests.post(start_url, data=data, headers=headers, timeout=15)
                except:
                    continue
                print(response.text)
                if response.text[0] == '(' and response.text[-1] == ')':
                    json_obj = json.loads(response.text[1:-1])
                else:
                    json_obj = json.loads(response.text)

                for item in json_obj['rows']:
                    CityCode = item['CityCode']
                    CityName = item['CityName']
                    AreaCode = item['AreaCode']
                    AreaName = item['AreaName']
                    EntCode = item['EntCode']
                    EntName = item['EntName']
                    EntTypeName = item['EntTypeName']
                    obj = {
                        'ip': ip,
                        'CityCode': CityCode,
                        'CityName': CityName,
                        'AreaCode': AreaCode,
                        'AreaName': AreaName,
                        'EntCode': EntCode,
                        'EntName': EntName,
                        'EntTypeName': EntTypeName,
                    }
                    for key in obj.keys():
                        if obj[key] == None:
                            obj[key] = ''
                    if EntCode not in id_list:
                        item_list.append(obj)
                        id_list.append(EntCode)





    for item in item_list:
        print(item)
        with open('shandong_id.txt','a') as f:
            save_res = item['ip']+','+item['CityCode']+','+item['CityName']+','+item['AreaCode']+','+item['AreaName']+','+item['EntCode']+','+item['EntName']+','+item['EntTypeName']+'\n'
            print(save_res)
            f.write(save_res)


if __name__ == '__main__':
    start()