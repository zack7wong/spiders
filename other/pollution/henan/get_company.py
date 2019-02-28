#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

id_list = []
url = 'http://www.hnep.gov.cn:98/ashx/GetSiteInfo.ashx?type=1&regioncode=&enptype=&enpname=&enpcode=&infoyear=2014'
response = requests.get(url)
print(response.text)
json_obj = json.loads(response.text)
for data in json_obj:
    # print(data)
    EnpName = data['EnpName']
    EnpCode = data['EnpCode']
    EnterTypeName = data['EnterTypeName']
    InfoYear = str(data['InfoYear'])

    start_url = 'http://www.hnep.gov.cn:98/EnpInfo.aspx?EnpCode={EnpCode}&InfoYear={InfoYear}'.format(EnpCode=EnpCode,InfoYear=InfoYear)
    save_res = EnpName+','+EnpCode+','+EnterTypeName+','+InfoYear+','+start_url+'\n'
    if EnpCode in id_list:
        continue
    else:
        id_list.append(EnpCode)
        print(save_res)
        with open('2014.txt','a') as f:
            f.write(save_res)