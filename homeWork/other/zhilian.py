#!/usr/bin/env python
# -*- coding:utf-8 -*-

#导入包
import requests
import json
import xlwt

#初始url
URL = 'https://fe-api.zhaopin.com/c/i/sou?start={pageToken}&pageSize=90&cityId=540&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=java&kt=3&_v=0.46804333&x-zp-page-request-id=8a59888ce1fd498bbfc9106fa6ac49a6-1545295956298-262292'

workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet('My Worksheet')

sheet.write(0, 0, '职位')
sheet.write(0, 1, '薪资')
sheet.write(0, 2, '经验')

#页数
num = 1
for i in range(10):
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
            # city = data['city']['display']
            workingExp = data['workingExp']['name']
            # eduLevel = data['eduLevel']['name']
            # company = data['company']['name']
            # res = name+','+salary+','+city+','+workingExp+','+eduLevel+','+company+'\n'
            res = name +','+salary+','+workingExp+'\n'
            print(res)
            #写文件
            sheet.write(num, 0, name)
            sheet.write(num, 1, salary)
            sheet.write(num, 2, workingExp)
            num +=1
        workbook.save('res.xls')
    except:
        continue