#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
from lxml.etree import HTML
import time
import db
import re
from urllib.parse import quote

headers = {
    'Pragma': "no-cache",
    'Origin': "http://www.hnep.gov.cn:98",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Connection': "keep-alive",
    'X-MicrosoftAjax': "Delta=true",
    'cache-control': "no-cache",
    'Postman-Token': "345abaf8-6c2e-4be1-b82a-996ca26b38f8"
    }

get_headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Host': "www.hnep.gov.cn:98",
    'Pragma': "no-cache",
    'Referer': "http://www.hnep.gov.cn:98/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "8d44582a-9b61-4d57-a009-00dd8b5835d7"
    }

def get_date(year):
    if year == 2019:
        month_list = [1, 2]
    else:
        month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    fun = lambda year, month: list(range(1, 1+time.localtime(time.mktime((year,month+1,1,0,0,0,0,0,0)) - 86400).tm_mday))

    date_list = []
    for month in month_list:
        day_list = fun(year, month)
        for day in day_list:
            save_res = str(year)+'-'+str(month)+'-'+str(day)
            # print(save_res)
            date_list.append(save_res)
    # print(date_list)
    return date_list

def get_start_VIEWSTATE(url):
    response = requests.get(url,headers=get_headers,timeout=10)
    # print(response.text)
    html = HTML(response.text)
    rd_DataType = html.xpath('string(//input[@id="rd_DataType_0"]/@value)')
    EntTypeName = html.xpath('string(//span[@id="rd_DataType"]/label/text())')
    __EVENTVALIDATION = re.search('id="__EVENTVALIDATION" value="(.*?)"',response.text).group(1)
    __EVENTVALIDATION = quote(__EVENTVALIDATION).replace('/','%2F')
    __VIEWSTATE = re.search('id="__VIEWSTATE" value="(.*?)"',response.text).group(1)
    __VIEWSTATE = quote(__VIEWSTATE).replace('/','%2F')
    # print(__VIEWSTATE)
    # print(__EVENTVALIDATION)
    # print(rd_DataType)

    return __VIEWSTATE,__EVENTVALIDATION,rd_DataType,EntTypeName

def parse(html,EntTypeName,item):

    title = item['title']
    EnpCode = item['EnpCode']
    EnterTypeName = item['EnterTypeName']

    tr_list = html.xpath('//table[@id="tbdata_auto"]//tr')
    # 企业名称、污染源类型（废水、废气）、检测日期、监测项目、排放口及监测点位、监测结果、单位、执行标准名称
    bianzhunName = ''
    for tr in tr_list[2:]:
        try:
            jianceTime = tr.xpath('string(./td[2])').strip()
            jianceProject = tr.xpath('string(./td[3])').strip()
            jianceAddress = tr.xpath('string(./td[4])').strip()
            jianceValue = tr.xpath('string(./td[5])').strip()
            danwei = tr.xpath('string(./td[6])').strip()

            td_list = tr.xpath('./td')
            # print(len(td_list))
            if len(td_list) == 14:
                bianzhunName = tr.xpath('string(./td[7])').strip()

            print(title, EntTypeName, jianceTime, jianceProject, jianceAddress, jianceValue, danwei, bianzhunName)

            sql = "insert into henan(title, EntTypeName, jianceTime, jianceProject, jianceAddress, jianceValue, danwei, bianzhunName)" \
                  " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (title, EntTypeName, jianceTime, jianceProject, jianceAddress, jianceValue, danwei, bianzhunName)
            dbclient.save(sql)
        except:
            continue


def start(item):
    InfoYear = item['InfoYear']

    date_list = get_date(int(InfoYear))
    for date in date_list:
        try:
            print('当前日期：'+date)
            startDate = date
            endDate = date
            start_url = item['url']

            try:
                __VIEWSTATE,__EVENTVALIDATION,rd_DataType,EntTypeName = get_start_VIEWSTATE(start_url)
            except:
                pass

            body = 'ScriptManager1=UpdatePanel2%7CAsp_AutoData&rd_DataType={rd_DataType}&txtStartDate_autoData={startDate}&txtEndDate_autoData={endDate}&Asp_AutoData_input={pageToken}&rd_SiteType={rd_DataType}&txtStartDate_handData=2019-02-20&txtEndDate_handData=2019-02-27&txtStartDate_NoiseData=2019&txtStartDate_otherData=2019-02-20&txtEndDate_otherData=2019-02-27&txt_reason=2019&txt_monplan=2019&txtyearreport=2019&__VIEWSTATE={__VIEWSTATE}&__VIEWSTATEGENERATOR=239CFCF6&__EVENTTARGET=Asp_AutoData&__EVENTARGUMENT=&__EVENTVALIDATION={__EVENTVALIDATION}&__ASYNCPOST=true&Asp_AutoData=%E7%A1%AE%E5%AE%9A'

            #获取第一页
            data = body.format(startDate=startDate, endDate=endDate, pageToken=1, __EVENTVALIDATION=__EVENTVALIDATION, __VIEWSTATE=__VIEWSTATE,rd_DataType=rd_DataType)
            # print(start_url)
            # print(data)
            try:
                response = requests.post(start_url, headers=headers, data=data,timeout=10)
            except:
                continue
            html = HTML(response.text)
            if '无数据！'in response.text:
                print('无数据')
                continue

            #获取总页数
            try:
                totalPage = int(re.search('共(\d+)页',response.text).group(1))
                print('总页数：'+str(totalPage))
            except:
                totalPage = 1


            #处理第一页
            print('当前页：1')
            parse(html,EntTypeName,item)

            #处理剩余页数
            for i in range(2,totalPage+1):
                print('当前页：'+str(i))
                data = body.format(startDate=startDate, endDate=endDate, pageToken=i, __EVENTVALIDATION=__EVENTVALIDATION,__VIEWSTATE=__VIEWSTATE, rd_DataType=rd_DataType)
                try:
                    response = requests.post(start_url, headers=headers, data=data,timeout=10)
                except:
                    continue
                html = HTML(response.text)
                parse(html, EntTypeName, item)

        except:
            continue



if __name__ == '__main__':
    #郑州新力电力有限公司,41010261471114-9,废气国控,2014,http://www.hnep.gov.cn:98/EnpInfo.aspx?EnpCode=41010261471114-9&InfoYear=2014
    dbclient = db.MysqlClient()
    item_list = []
    with open('2014a.txt') as f:
        results = f.readlines()
        for res in results:
            title = res.split(',')[0]
            EnpCode = res.split(',')[1]
            EnterTypeName = res.split(',')[2]
            InfoYear = res.split(',')[3]
            url = res.split(',')[4].strip()
            obj = {
                'title':title,
                'EnpCode':EnpCode,
                'EnterTypeName':EnterTypeName,
                'InfoYear':InfoYear,
                'url':url,
            }
            item_list.append(obj)

    for item in item_list:
        print(item)
        try:
            start(item)
        except:
            continue