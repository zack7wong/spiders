#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
import json

#初始url
URL = 'https://fe-api.zhaopin.com/c/i/sou?start={pageToken}&pageSize=90&cityId=540&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=Python&kt=3&_v=0.46804333&x-zp-page-request-id=8a59888ce1fd498bbfc9106fa6ac49a6-1545295956298-262292'

#页数
for i in range(25):
    #异常处理
    try:
        #翻页值
        pageToken = str(i*90)
        start_url = URL.format(pageToken=pageToken)
        #开始请求
        response = requests.get(start_url,timeout=10)
        #解析返回的json数据
        json_obj = json.loads(response.text)
        #for循环处理每个字段
        for data in json_obj['data']['results']:
            name = data['jobName']
            salary = data['salary']
            city = data['city']['display']
            workingExp = data['workingExp']['name']
            eduLevel = data['eduLevel']['name']
            company = data['company']['name']
            res = name+','+salary+','+city+','+workingExp+','+eduLevel+','+company+'\n'
            print(res)
            #写文件
            with open('results.csv','a') as f:
                f.write(res)
    except:
        continue